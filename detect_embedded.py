import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.stats import entropy
from collections import defaultdict

def calculate_histogram(image_path):
    image = Image.open(image_path)
    image = image.convert('L')
    histogram, _ = np.histogram(image, bins=256, range=(0,255))
    return histogram


def compare_histograms(hist1, hist2):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title('Original Histogram')
    plt.bar(range(256), hist1, color='blue', alpha=0.7)
    plt.subplot(1, 2, 2)
    plt.title('Suspected Histogram')
    plt.bar(range(256), hist2, color='red', alpha=0.7)
    plt.show()


def pixel_distribution(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    pixels = np.array(image)
    print(f"Image shape: {pixels.shape}")

    rgb_distribution = np.zeros((256,256,256), dtype=int)
    total_pixels = pixels.shape[0] * pixels.shape[1]
    print(f"Total pixels to process: {total_pixels}")

    processed_pixels = 0
    for row in pixels:
        for pixel in row:
            r, g, b = pixel
            rgb_distribution[r, g, b] += 1
            processed_pixels += 1

            if processed_pixels % 100000 == 0:
                print(f"Processed {processed_pixels} / {total_pixels} pixels")

    return rgb_distribution

def compare_distributions(distribution1, distribution2):
    distribution1_flat = distribution1.flatten()
    distribution2_flat = distribution2.flatten()

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original RGB Distribution")
    plt.hist(distribution1_flat, bins=256, range=(0, np.max(distribution1_flat)), color='blue', alpha=0.7)
    plt.subplot(1, 2, 2)
    plt.title("Suspected RGB Distribution")
    plt.hist(distribution2_flat, bins=256, range=(0, np.max(distribution2_flat)), color='red', alpha=0.7)
    plt.show()

def calculate_entropy(image_path):
    image = Image.open(image_path)
    image = image.convert('L')
    pixels = np.array(image).flatten()
    histogram, _ = np.histogram(pixels, bins=256, range=(0,255))
    return entropy(histogram, base=2)


#compare historgrams, compare changes, compare entropy
def steganalysis(image_path, suspected_image_path):
    print("Starting steganalysis...")

    # Calculate and compare histograms
    print("Calculating histograms...")
    hist1 = calculate_histogram(image_path)
    hist2 = calculate_histogram(suspected_image_path)
    compare_histograms(hist1, hist2)

    # Calculate and compare LSB changes
    print("Calculating LSB changes for original image...")
    lsb_changes1 = pixel_distribution(image_path)
    print("Calculating LSB changes for suspected image...")
    lsb_changes2 = pixel_distribution(suspected_image_path)
    compare_distributions(lsb_changes1, lsb_changes2)

    # Calculate and compare entropy
    print("Calculating entropy...")
    entropy1 = calculate_entropy(image_path)
    entropy2 = calculate_entropy(suspected_image_path)
    print(f"Original Entropy: {entropy1}")
    print(f"Suspected Entropy: {entropy2}")

    if entropy2 > entropy1:
        print("Higher entropy detected in suspected image, indicating possible hidden data.")
    else:
        print("No significant increase in entropy detected.")


def main():
    image_path = 'flowers.png'
    suspected_image_path = 'encrypted_flowers.png'
    steganalysis(image_path, suspected_image_path)

if __name__ == '__main__':
    main()









        