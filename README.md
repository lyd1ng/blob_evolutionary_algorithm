# blob_evolutionary_algorithm
A small evolutionary algorithm adjusting the form and behaviour of blobs.

# Inspiration
I just wanted to play with an evolutionary algorithm.
This is not usefull in any way.
The evolutionary alorithm works continious and doesnt use
generations. The time a blob is alive as well as the health
of the blob increases the change for reproduction.

# Blob
The blob is the subject of this evolutionary algorithm and
is specified by two genoms, the size and the health_threshold.
The size specifies the speed, the costs while moving
and the costs for resting. Costs in this context means
the health_decrease per second.
The moving costs increases while the rest costs decreases
exponentially for larger sizes.
Blobs can only eat food pieces smaller than their selfe
and or only seeking for eatable food pieces.
Blobs starts to seek new food if the health drops below
the health threshold.

# Food
The food is dropped randomly across the screen.
The frequence of food dropps is controlled with a pygame
timer from main.py throwing a FEED_EVENT.
Default is a 150ms delay between every food drop.

# Graphics
The graphical output is realized with pygame using primitivs
and DejaVuSansMono.


![alt text][logo]

[logo]: excerpt.png
