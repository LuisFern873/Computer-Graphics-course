
"""
Explicación:
El número de triangulaciones de un polígono con n lados estado dado por el C_{n-2} número catalán

C_{n} = ( 1 / (n + 1)) Combinatoria(2n n) = 2n! / (n + 1)! n!

Utilizo programación dinámica para computar el numero requerido 

"""

def numTriangulations(n):
    if n < 3:
        return 0
    catalan_index = n - 2

    catalan_numbers = [0] * (catalan_index + 1)
    catalan_numbers[0] = 1

    # Fill the array using the recursive relation
    for i in range(1, catalan_index + 1):
        catalan_numbers[i] = 0
        for j in range(i):
            catalan_numbers[i] += catalan_numbers[j] * catalan_numbers[i - 1 - j]
    
    return catalan_numbers[catalan_index]

# Example usage:
n = 9
print(f"Number of triangulations of a {n}-sided polygon: {numTriangulations(n)}")
