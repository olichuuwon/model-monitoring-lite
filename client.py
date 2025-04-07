import json
import requests
import time


def query_triton(prompt, max_tokens=50, temperature=0.7):
    """
    Query the OPT-125M model hosted on Triton Inference Server

    Args:
        prompt (str): The input text to generate from
        max_tokens (int): Maximum number of tokens to generate
        temperature (float): Sampling temperature

    Returns:
        str: The generated text
    """
    url = "http://localhost:8000/v2/models/opt/generate"

    payload = {
        "text_input": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    headers = {"Content-Type": "application/json"}

    print(f"Sending request with prompt: '{prompt}'")
    start_time = time.time()

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    end_time = time.time()
    elapsed = end_time - start_time

    if response.status_code == 200:
        result = response.json()
        output_text = result.get("text_output", "")
        print(f"\nGeneration completed in {elapsed:.2f} seconds")
        print(f"Generation rate: {max_tokens/elapsed:.2f} tokens/second")
        return output_text
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


if __name__ == "__main__":
    # Example prompts to test
    prompts = [
        "Once upon a time in a land far away",
        "The best way to learn programming is",
        "In the year 2050, technology will",
        "The three most important qualities of a good leader are",
    ]

    print("OPT-125M Triton Client Tester")
    print("=" * 40)

    for i, prompt in enumerate(prompts, 1):
        print(f"\nTest {i}/{len(prompts)}")
        output = query_triton(prompt)
        if output:
            print(f"\nOutput: {output}")

        # Wait a bit between requests when running on CPU
        if i < len(prompts):
            print("\nWaiting for next request...")
            time.sleep(2)
