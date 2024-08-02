### Code Authorship Attribution:
To solve this problem using Large Language Models (LLMs), we fine-tune five encoder-only LLMsS such as CodeBERT, ContraBERT_C, ContraBERT_G, GraphCodeBERT, and UnixCoder. These models are fine-tuned on the datasets located in the `Datasets` directory.

### Code Authorship Verification:
The methodology of our code authorship verification is as follows:

![](./Verification/AV-Methodology.png)

`Verification` folder contains the all data and code for the all experiments we have conducted. To replicate our results, go to `Verification` directory -

- To verify code authorship using Gemini, run `python3 av_gemini.py {dataset_name} {sample}`. `{dataset_name}` should be replaced with the any of the datasets name found in `Datasets` folder. The value of `{sample}` should be `positive` or `negative`.

- Similarly, run `python3 av_gpt-4.py {dataset_name} {sample}` to verify code authorship using GPT-4.

**Note:** Before running `av_gemini.py` or `av_gpt-4.py`, please replace the respective API_Key.

