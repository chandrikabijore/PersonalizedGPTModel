import os # os, time: built-in modules for file path and time operations
import time
import openai # openai: OpenAI's Python library for API interaction
from openai import OpenAI 
from dotenv import load_dotenv # load_dotenv: loads variables from .env file into environment variables.

# Load environment variables from .env file .env file se OPENAI_API_KEY load karta hai. Agar key nahi milti, toh error throw karta hai:
load_dotenv()   

# Initialize the client with API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please add it to .env file")

openai.api_key = "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"
client = OpenAI(api_key=api_key)

print("✅ Successfully initialized OpenAI client")

# Add error handling for file upload
try:
    print("📤 Uploading training file...")
    with open("FinalData2804.jsonl", "rb") as f:
        upload_response = client.files.create(
            file=f,
            purpose="fine-tune"
        )
    training_file_id = upload_response.id
    print(f"✅ Successfully uploaded training file. File ID: {training_file_id}")
except FileNotFoundError:
    print("❌ Error: FinalData2804.jsonl not found in the current directory")
    exit(1)
except Exception as e:
    print(f"❌ File upload failed: {str(e)}")
    exit(1)

# Fine-tune the model
print("🚀 Starting fine-tuning job...")
try:
    fine_tune_response = client.fine_tuning.jobs.create(
        training_file=training_file_id,
        model="gpt-3.5-turbo",
        hyperparameters={
            "n_epochs": 10,                     # or 12
            "learning_rate_multiplier": 0.05,   # lower for quality
            "batch_size": 4,                    # small dataset
        }
    )
    fine_tune_job_id = fine_tune_response.id
    print(f"✅ Fine-tuning job created. Job ID: {fine_tune_job_id}")
except Exception as e:
    print(f"❌ Failed to create fine-tuning job: {str(e)}")
    exit(1)

# Step 3: Monitor job status
print("🔄 Monitoring fine-tuning progress...")
max_wait_time = 10800  # 3 hours
start_time = time.time()
last_status = ""
while True:
    try:
        status_response = client.fine_tuning.jobs.retrieve(fine_tune_job_id)
        status = status_response.status

        # Only print status if it has changed
        if status != last_status:
            print(f"📡 Status: {status}")
            last_status = status

            # Print progress if available
            if hasattr(status_response, 'trained_tokens') and status_response.trained_tokens:
                print(f"   Tokens processed: {status_response.trained_tokens}")

        if status in ["succeeded", "failed"]:
            break

        if time.time() - start_time > max_wait_time:
            print("❌ Timeout: Fine-tuning took too long")
            break

        # Check less frequently as training progresses
        if status == "validating_files":
            time.sleep(5)
        else:
            time.sleep(30)

    except Exception as e:
        print(f"⚠️ Error checking status: {str(e)}")
        time.sleep(60)  # Wait longer if there's an error

# Step 4: Get model ID if successful
if status == "succeeded":
    fine_tuned_model = status_response.fine_tuned_model
    print("\n🎉 Fine-tuning completed successfully!")
    print(f"🔧 Model name: {fine_tuned_model}")
    print("\nYou can now use this model with the OpenAI API by specifying the model name above.")

    # Save model info to a file
    with open("model_info.txt", "w") as f:
        f.write(f"Fine-tuned model: {fine_tuned_model}\n")
        f.write(f"Job ID: {fine_tune_job_id}\n")
        f.write(f"Training file: {training_file_id}\n")
        f.write(f"Completed at: {time.ctime()}\n")

    print("\n📝 Model information has been saved to 'model_info.txt'")
else:
    print("\n❌ Fine-tuning failed. Check the logs below for more information.")

# Show detailed training logs
print("\n📜 Retrieving training logs...")
try:
    events = client.fine_tuning.jobs.list_events(id=fine_tune_job_id, limit=50)  # Get last 50 events

    if not events.data:
        print("No log events found.")
    else:
        print("\n=== TRAINING LOGS ===")
        for event in reversed(events.data):  # Show most recent first
            timestamp = event.created_at
            message = event.message
            print(f"[{timestamp}] {message}")
        print("===================")

        # Save logs to file
        with open("training_logs.txt", "w") as f:
            for event in reversed(events.data):
                f.write(f"[{event.created_at}] {event.message}\n")
        print("📝 Full logs have been saved to 'training_logs.txt'")

except Exception as e:
    print(f"⚠️ Error retrieving logs: {str(e)}")
    print("You can check the logs in the OpenAI dashboard if needed.")

print("\n✅ Script completed. Check the logs above for any issues or next steps.")