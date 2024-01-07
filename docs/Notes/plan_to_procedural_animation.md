# With Raycasting

- [x] Cast a ray to find the target position
- [x] Make the feet follow that position

![ray_casting](ray_casting.png)

## Pseudo code for raycasting of the leg target pos

* Place the S point in the desired start position
* While S.y > player.y
	* For each block
		* If S collides with the block and block.top < initial S.y
			* S.y = block.top
			* break both loops
		* S.y += STEP_CONSTANT
* If S.y < player.y
	* S.y = player.y

- [x] set the lerp pos to the target pos is distance from hip to lerp is bigger than leg

# With sinusoidal curve


