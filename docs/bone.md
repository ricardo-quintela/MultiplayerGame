# The Bone class
  
### \_\_init\_\_  
  
**Signature:**  
  
>```__init__(self, x: int, y: int, length: float, angle: float, name: str = "") -> None```  
  
**Description:**  
  
>Constructor of the class Bone  
  
**Arguments:**  
  
>```x``` (```int```): the x coord of the bone  
>```y``` (```int```): the y coord of the bone  
>```length``` (```float```): the length of the bone  
>```angle``` (```float```): the angle of the ```bone``` (degrees)  
>```name``` (```str```): the name of the bone  
>  
  
  
### calculate\_b  
  
**Signature:**  
  
>```calculate_b(self) -> Vector2```  
  
**Description:**  
  
>Calculates the B point of the bone based on the length and the angle  
  
**Returns:**  
  
>Vector2: the cartesian coordinates of point b
  
  
  
### bind  
  
**Signature:**  
  
>```bind(self, target)```  
  
**Description:**  
  
>Bind this bone to a joint  
>  
>The target point must be a mutable object  
  
**Arguments:**  
  
>```target``` (list, Vector2): the point to bind the joint to  
>  
  
  
### follow  
  
**Signature:**  
  
>```follow(self, target: tuple)```  
  
**Description:**  
  
>Makes the bone align and follow a given target  
  
**Arguments:**  
  
>```target``` (```tuple```): the position of the target  
>  
  
  
### update  
  
**Signature:**  
  
>```update(self)```  
  
**Description:**  
  
>Updates the bone position  
  
  
### blit  
  
**Signature:**  
  
>```blit(self, canvas: Surface)```  
  
**Description:**  
  
>Draw the bone on the given Surface  
  
**Arguments:**  
  
>```canvas``` (```Surface```): the Surface where to draw the bone  
>  
  
  
