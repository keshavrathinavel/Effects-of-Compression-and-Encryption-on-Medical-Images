# Effects-of-Compression-and-Encryption-on-Medical-Images


# Conventional Practices

1. **Encryption** - AES is broadly used in a wide range of applications, from securing web traffic (HTTPS) to encrypting personal and corporate data, due to its reliability, speed, and security.
2. **Secure Data Transfer Protocols**
3. **Data Integrity and Authentication**
4. **Access Control**
5. **Audit Trails**

# AES in CBC (Cipher Block Chaining)

### **Key Features of AES:**

- **Symmetric Key Encryption**: The same key is used for both encrypting and decrypting the data.
- **Block Cipher**: AES encrypts data in fixed-size blocks (128 bits).
- **Key Sizes**: AES can use keys of three different sizes: 128, 192, or 256 bits.

### **Working of AES Algorithm:**

1. **Key Expansion (Key Schedule)**: AES first expands the initial key into a series of round keys. The number of rounds and round keys depends on the key size: 10 rounds for a 128-bit key.
2. **Initial Round**:
- ************************************************Initialisation Vector************************************************ - The IV is a random value of the size of the block (128 bits or 16 bytes). Does not need to be secret but should be unpredictable and unique for each encryption.
- **************Dividing Data into Blocks************** - The plaintext is divided into blocks, each of 128 bits. If the last block is not complete, it is padded to reach the required block size.
1. **Main Rounds**: Each main round consists of four steps:
    - **SubBytes (Substitution)**: Each byte in the state is replaced with another according to a fixed table (the S-box).
    - **ShiftRows**: Rows of the state are shifted cyclically. The first row is not shifted, the second row is shifted one byte to the left, the third row two bytes, and the fourth row three bytes.
    - **MixColumns**: Each column of the state is multiplied with a fixed polynomial in the Galois field. This step mixes the bytes within each column.
    - **AddRoundKey**: Each byte of the state is combined again with the round key using bitwise XOR.
2. **Final Round**: The final round of AES is slightly different, omitting the MixColumns step. It includes:
    - SubBytes
    - ShiftRows
    - AddRoundKey

### **Decryption Process:**

- The decryption process in AES reverses the steps taken during encryption.
- It uses the inverse operations for each step (Inverse ShiftRows, Inverse SubBytes, Inverse MixColumns) and applies the round keys in reverse order.

### **Security:**

- AES is considered highly secure. Its strength lies in the combination of the SubBytes step, which ensures confusion (each output bit depends on multiple input bits in a complex way), and the MixColumns step, which ensures diffusion (spreading the influence of a single input bit over many output bits).
- Chain Reaction - each block’s encryption depends on the previous block. This means that a change in one block affects all subsequent blocks, both in encryption and decryption.
- The repeated rounds and combination of operations provide strong resistance against various cryptographic attacks, including brute force attacks, though the effort to crack AES increases exponentially with key size.

![Untitled](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/Untitled.png)

```python
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Key used for encryption
key = get_random_bytes(16)

def encrypt_image(input_file, output_file, key):
    print("Encrypting files")
    cipher = AES.new(key, AES.MODE_CBC)
    with open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            f_out.write(cipher.iv)
            data = f_in.read()
            f_out.write(cipher.encrypt(pad(data, AES.block_size)))

def decrypt_image(input_file, output_file, key):
    print("Decrypting files")
    with open(input_file, 'rb') as f_in:
        iv = f_in.read(16)  # AES block size is 16 bytes
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(output_file, 'wb') as f_out:
            data = f_in.read()
            f_out.write(unpad(cipher.decrypt(data), AES.block_size))
```

**************************************Initialisation Vector************************************** - The `cipher.iv` ensures that if the same data is encrypted multiple times, the ciphertext will be different each time. 

**************Padding************** - The `data` is then padded to ensure its size is a multiple of the AES block size (16 bytes). This is necessary because AES is a block cipher that operates on fixed-size blocks of data.

![Untitled](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/Untitled%201.png)

# Pillow (PIL)

### JPEG Compression

- **Lossy Compression:** JPEG is a popular format that uses lossy compression.
- **Discrete Cosine Transform (DCT):** It transforms spatial domain data (pixels) into frequency domain data.
    
    ![Untitled](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/Untitled%202.png)
    
- **Quantization:** After DCT, the coefficients are quantised to reduce the precision of the high-frequency components, which is less noticeable to the human eye.
- **Entropy Encoding:** Finally, the quantised values are compressed using Huffman coding or arithmetic coding.

![Untitled](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/Untitled%203.png)

![Untitled](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/Untitled%204.png)

```python
from PIL import Image

def compress_image(image_path, output_path, quality):
    """
    Compress an image, retaining its original dimensions for the learning mode
    but reducing file size on disk.
    :param image_path: Path to the original image.
    :param output_path: Path to save the compressed image.
    :param quality: Quality level for compression, between 1 (worst) and 95 (best). 85 is recommended.
    """
    with Image.open(image_path) as img:
        img.save(output_path, 'JPEG', optimize=True, quality=quality)
```

# Results

## Without Compression-Encryption

### Before LR Plateau and Early Stopping Callback

![Untitled](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/Untitled%205.png)

![Untitled](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/Untitled%206.png)

### After LR Plateau and Early Stopping Callback

![raw_after_tuning.png](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/raw_after_tuning.png)

![raw_plots_after_tuning.png](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/raw_plots_after_tuning.png)

![raw_bar_graph.png](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/raw_bar_graph.png)

******Tabulated Results******

| Model | Accuracy |
| --- | --- |
| DenseNet 161 | 0.854688 |
| ResNet 152 | 0.896875 |
| VGG 19 | 0.865625 |
| Ensemble Learning | 0.835938 |

### Learnings

- ************************DenseNet 161************************: It shows volatility in accuracy, with a general increasing trend, suggesting some learning but possibly also some overfitting as it doesn't stabilize.
- ********************ResNet 152********************: The accuracy of this model also fluctuates but trends downward after the initial epochs, which might indicate that the model is not learning effectively or is overfitting to the training data.
- ************VGG 19************: This model starts with a relatively high accuracy and maintains a stable performance throughout the training.
- **Ensemble Learning**: This model's performance is relatively stable with high accuracy which suggests that ensemble methods are providing consistent predictive performance.

## Compression-Encryption Performed on Images

### Before LR Plateau and Early Stopping Callback

![img.png](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/img.png)

### After LR Plateau and Early Stopping Callback

![after_tuning.png](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/after_tuning.png)

![after_tuning_with_ensemble.png](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/after_tuning_with_ensemble.png)

**********************************Tabulated Results**********************************

| Model | Accuracy |
| --- | --- |
| DenseNet 161 | 0.801562 |
| ResNet 152 | 0.834375 |
| VGG 19 | 0.862500 |
| Ensemble Learning | 0.817187 |

### Highest Accuracy and Lowest Loss

![high_low_after_tuning.png](Effects%20of%20Compression%20and%20Encryption%20on%20Images%207a6c853b89ab4fb3980a998db4b7ca34/high_low_after_tuning.png)

### Learnings

- **DenseNet 161** shows fluctuating accuracy, indicating potential instability or overfitting in certain epochs.
- **ResNet 152** demonstrates more consistent accuracy, with a slight upward trend, suggesting steady learning.
- **VGG 19** exhibits high and relatively stable accuracy, indicating effective learning and generalisation.
- **Ensemble Learning** shows a significant improvement over epochs, starting low but eventually surpassing other models, which is characteristic of ensemble methods that often start slowly but improve significantly as more models are combined.

### Inference

- The **Ensemble Learning** approach seems to be the most effective in terms of both accuracy and loss, especially in later epochs. This suggests that combining multiple models is beneficial for this particular task.
- **VGG 19** maintains a strong performance consistently, making it a reliable choice.
- **ResNet 152** offers good and stable performance, though not reaching the peaks of VGG 19 or Ensemble Learning.
- **DenseNet 161**, while effective, appears to be less stable compared to the others. Being a new architecture, further investigation can help this case.

### Remarks

********With the use of LR Plateau and Early Stopping Callback********

- The validation accuracy appears more stable across epochs, particularly for the Ensemble model, which suggests that the use of learning rate plateau and early stopping has likely contributed to a more consistent learning process.
- The validation loss for all models is reduced significantly and remains lower and more stable compared to the first image. This is a strong indication that the callbacks have helped in preventing overfitting and have improved the generalisation of the models.

# Conclusion

## Conclusion

- All models start with significantly lower validation accuracy after the images have been **compressed, encrypted, decrypted, and decompressed**. This suggests that these operations have degraded the quality of the images to some extent, making it challenging for the models to classify them correctly.
- There is a general trend of increasing validation loss across all models, with DenseNet 161 displaying the highest loss. This shows that the operations have affected the model's ability to generalize, leading to poor performance on the compressed and encrypted dataset.

**Effects of Compression, Encryption, Decryption, and Decompression:**

- These operations seem to introduce some level of noise or information loss in the images, as inferred from the increased volatility and decreased performance in the plots.
- The application of learning rate adjustments and early stopping mechanisms can mitigate some of the negative impacts of these operations by preventing overfitting and promoting better convergence during training.
