# Leaky AES

## Description

None

## Solution

Đây là một bài AES-CTR nonce reuse khá cơ bản, đề cho ta một cặp plaintext - ciphertext nên ta có thể recover lại keystream, từ đó chỉ việc xor lại encrypted_flag là ra.

Tuy nhiên bài này khá "khốn nạn" là flag bị sai (thiếu "C" trong "ASCIS")

Code mình để [ở đây](./sol.py)

**Flag: ASCIS{Congratulate_and_W3lc0me_t0_ASCIS_CRYPT0_chall}**