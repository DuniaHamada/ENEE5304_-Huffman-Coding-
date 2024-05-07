import heapq
from collections import Counter, defaultdict

from math import log2  
#Finding the number of characters in the story and their frequency
def calculate_frequencies(text):
    frequencies = Counter(text)
    return frequencies
#Calculating the probabilities of these characters
def calculate_probabilities(frequencies, total_characters):
    probabilities = {char: freq / total_characters for char, freq in frequencies.items()}
    return probabilities

def huffman_coding(probabilities):
    heap = [[weight, [char, ""]] for char, weight in probabilities.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    huffman_codes = {char: code for char, code in heap[0][1:]}
    return huffman_codes

def calculate_bits_needed(text, encoding):
    return sum(len(encoding[char]) for char in text)

def main():
    with open(r"/Users/noormacbook/Desktop/Coding/Assigment/story.txt", "r") as file:

        story = file.read().replace('\n', '').lower()

    total_characters = len(story)
    frequencies = calculate_frequencies(story)
    probabilities = calculate_probabilities(frequencies, total_characters)
    #Finding the entropy of the alphabet:
    entropy = sum(-p * (p and log2(p)) for p in probabilities.values())
    #generate Huffman codewords for the characters
    huffman_codes = huffman_coding(probabilities)
    #Calculating the number of bits needed to encode the full story
    n_ascii = total_characters * 8
    #Determining the total number of bits needed for Huffman encoding 
    n_huffman = calculate_bits_needed(story, huffman_codes)
    compression_percentage = ((n_ascii - n_huffman) / n_ascii) * 100


    # Using string formatting to create a single table
    header = f"{'Character':<12}{'Frequency':<12}{'Probability':<15}{'Entropy':<20}{'Huffman Code':<20}{'Bits Count':<12}"
    print(header)
    print('-' * len(header))
    for char in sorted(frequencies.keys()):
        freq = frequencies[char]
        prob = probabilities[char]
        ent = -prob* log2(prob) if prob > 0 else 0
        code = huffman_codes[char]
        bits_count = len(code)
        print(f"{char:<12}{freq:<12}{prob:<15.4f}{ent:<15.4f}{code:<20}{bits_count:<12}")

    print("\nSummary:")
    print(f"{'Total Number Of Characters:':<30}{total_characters}")
    print(f"{'N_ASCII:':<30}{n_ascii} bits")
    print(f"{'N_Huffman:':<30}{n_huffman} bits")
    print(f"{'Average Bits/Character (Huffman):':<30}{n_huffman / total_characters:.2f} bits/character")
    print(f"{'Entropy:':<30}{entropy:.2f} bits/character")
    print(f"{'Compression Percentage:':<30}{compression_percentage:.2f}%")
if _name_ == "_main_":
    main()