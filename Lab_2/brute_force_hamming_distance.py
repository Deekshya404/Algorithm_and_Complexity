def hamming_distance(word1, word2):
    if len(word1) != len(word2):
        raise ValueError("Words must be of equal length")
    
    distance = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            distance += 1
    return distance

# Example
w1 = "karolin"
w2 = "kathrin"
print("Hamming Distance:", hamming_distance(w1, w2))