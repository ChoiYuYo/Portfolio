#include <iostream>
#include <cstring>
using namespace std;

int findMaxValue(int a[], int b) {
	int Max=a[0];
	for (int i = 1; i <b; i++) {
		if (Max <a[i]) 
			Max = a[i];
	}
	return Max;
}
char findMaxChar(char a[]) {
	char Max = a[0];
	int b = strlen(a);
	
	for (int i = 1; i < b; i++) {
		if (Max < a[i])
			Max = a[i];
	}
	return Max;
}
int main() {
	int arr[10] = { 3,24,82,95,34,26,51,62,36,9 };
	char str[] = "Game Over !";
	cout << findMaxValue(arr, 10)<<endl;
	cout << findMaxChar(str) << endl;
}