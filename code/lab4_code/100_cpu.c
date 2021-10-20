#include <stdio.h>
#include <stdlib.h>

int main (int argc, char** argv)
{
	float x = .00000002;
	float y = 2.0000002;
	for(int w =0; w <100000000; w++){
		for(int i =0; i < 10000000; i++){
			for(int j = 0; j <1000000; j++){
				y = (y + x/y)*y/y*y/y;
			}
		}
	}
}