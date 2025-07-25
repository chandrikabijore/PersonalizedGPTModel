# IK-Society Chatbot Fine-tuning

![Chatbot UI](Pictures/Img%20-%201.png)
![Chatbot UI](Pictures/Img%20-%202.png)

This project contains the code and data for fine-tuning a GPT-3.5-turbo model to create a chatbot for IK-Society.

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Training the Model

1. Prepare your training data in `FinalData2804.jsonl` (already provided)

2. Run the training script:
   ```bash
   python "01 - Data_training.py"
   ```

The script will:
- Upload your training data to OpenAI
- Start a fine-tuning job
- Monitor the training progress
- Save the model information to `model_info.txt`
- Save the training logs to `training_logs.txt`

<!-- OPENAI_API_KEY=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 -->

## Using the Fine-tuned Model

Once training is complete, you can use the fine-tuned model with the OpenAI API by specifying the model name that will be provided in the output and saved to `model_info.txt`.

## Files

- `01 - Data_training.py`: Script to fine-tune the model
- `FinalData2804.jsonl`: Training data in JSONL format
- `.env`: Stores your OpenAI API key (not tracked by git)
- `requirements.txt`: Python dependencies
- `model_info.txt`: Created after successful training, contains model details
- `training_logs.txt`: Detailed training logs

## Notes

- Training may take some time depending on the dataset size
- Monitor your OpenAI usage to avoid unexpected costs
- The model will be available in your OpenAI account after training

 
