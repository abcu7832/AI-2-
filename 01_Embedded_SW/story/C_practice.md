## [1-1] Hello C World! 인쇄하기
```c
#include <stdio.h>

void main(void)
{
	printf("Hello C World!");
}
```
## [1-2] printf 함수 연습
```c

```
## [1-3]  특수 기능 문자의 이해
```c
#include <stdio.h>

void main(void)
{
	printf("Hello C \n");
	printf("Return\rSa");
	printf("\nTab\tTab\n");
	printf("Back!\b");
	printf("Alarm!!!\a\n");
	printf("Character\0 Ghost\n");
	printf("\"Welcome!!\"");
}
```
## [1-4]  포맷지시어의 이해
```c
#include <stdio.h>

void main(void)
{
	printf("10진수 => %d\n", 100);
	printf("16진수 => %x와 %X\n", 0xF0, 0xF0);	
	printf("8진수 => %o\n", 034);	

	printf("%d, %x, %o\n", 100, 100, 100);
	printf("%d, %x, %o\n", 0x64, 0x64, 0x64);
	printf("%d, %x, %o\n", 0144, 0144, 0144);
	
	printf("%d, %#x, %#o\n", 100, 100, 100);
	printf("%d, 0x%x, 0%o\n", 100, 100, 100);
}
```
## [1-5] long long과 unsigned type 인쇄
```c
#include <stdio.h>

void main(void)
{
	printf("%u, %d\n", 100u, -100);
	printf("%lu, %ld, %lx\n", 100u, -100, 0x12345678L);
	printf("%llu, %lld, %llx\n", 100ULL, -100LL, 0x1234567890ABCDEFLL);
}
```
## [1-6] 문자와 문자열의 인쇄
```c
#include <stdio.h>

void main(void)
{
	printf("%c %c %c %c\n", 'A', 65, 0x41, '\x41');
	printf("%c %c %c\n", 'A'+1, 'B', 'C'-1);
	printf("%d %d %d %d\n", 1, 1+1, '1', '1'+1);
	printf("%c%c%c\n", 'A', 'B', 'C');
	printf("%s\n", "ABC\0DEF");
}
```
## [1-7] 실수형 상수 인쇄
```c
#include <stdio.h>

void main(void)
{
	printf("%f, %f \n", 3.14, -3.14);
	printf("%.16f, %.16f \n", 10.0f / 3.0f, 10.0 / 3.0);
	printf("%.5f, %.3f \n", 123.4567, 123.4567);
	printf("%2.1f, %10.2f, %5.2f \n", 123.45, 123.4567, 123.4567);
	printf("%10.2f, %010.2f \n", 123.4567, 123.4567);
}
```
## [2-1] 변수 선언과 초기화 연습
```c
#include <stdio.h>

void main(void)
{
	int width;
	int height, area;
	double circel_area, pi = 3.14, radious = 3;

	width = 10;
	height = 20;
	area = width * height;
	circel_area = pi * radious * radious;

	printf("%d * %d = %d\n", width, height, area);
	printf("%f * %f * %f = %f\n", pi, radious, radious, circel_area);
}
```
## [2-2] scanf 함수
```c
#include <stdio.h>

void main(void)
{
	int i;

	printf("Input:");
	scanf("%d", &i);

	printf("Your choice: %d\n", i);
}
```
## [2-3-1] 정수 여러개 받기 1
```c
#include <stdio.h>

void main(void)
{
	int a, b, c;

	scanf("%d%d%d", &a, &b, &c);
	printf("%d %d %d\n", a, b, c);
}
```
## [2-3-2] 정수 여러개 받기 2
```c
#include <stdio.h>

void main(void)
{
	int a, b, c;

	scanf("%d %d %d", &a, &b, &c);
	printf("%d %d %d\n", a, b, c);
}
```
## [2-4] 실수, 16진수 입력 받기
```c
#include <stdio.h>

void main(void)
{
	int a; 
	float b;

	scanf("%x %f", &a, &b);
	printf("0x%x %f\n", a, b);
}
```
## [2-5-1] 문자 입력 받기 1
```c
#include <stdio.h>

void main(void)
{
	char a, b;

	scanf("%c%c", &a, &b);
	printf("%c %c\n", a, b);
}
```
## [2-5-2] 문자 입력 받기 2
```c
#include <stdio.h>

void main(void)
{
	char a, b;

	scanf("%c %c", &a, &b);
	printf("%c %c\n", a, b);
}
```
## [2-6] 문자 두 번 입력 받기
```c
#include <stdio.h>

void main(void)
{
	char a, b;

	scanf("%c", &a);
	scanf("%c", &b);
	printf("%c %c\n", a, b);
}
```
## [2-7] 문자 두 번 입력 받기 개선
```c
#include <stdio.h>

void main(void)
{
	char a, b, c;

	scanf(" %c", &a);
	scanf(" %c %c", &b, &c);
	printf("%c %c %c\n", a, b, c);
}
```
## [2-8] 문자열을 입력받는 scanf
```c
#include <stdio.h>

void main(void)
{
	char a[101];
	char b[101];
		
	scanf(" %s     %s", a, b);
	printf("%s, %s\n", a, b);
}
```
## [2-9] 공백이 포함된 문자열 입력 받기
```c
#include <stdio.h>

void main(void)
{
	char a[101];
	char b[101];

	gets(a);
	gets(b);
	printf("%s, %s\n", a, b);
}
```
## [2-10] 다양한 입력 및 출력 연습
```c
#include <stdio.h>

void main(void)
{
	char name[31];
	int age;
	float height;
	char blood_type;
	char nationality[11];

	// 코드 작성

}
#endif
```
## [3-1] 사칙연산
```c
#include <stdio.h>

void main(void)
{
	int a = 10, b = 4;

	printf("a + b = %d\n", a + b);
	printf("a - b = %d\n", a - b);
	printf("a * b = %d\n", a * b);
	printf("a / b = %f\n", 10.0 / 4.0);
	printf("a / b = %d\n", a / b);
	printf("a %% b = %d\n", a % b);
}
```
## [3-2] 대입 연산
```c
#include <stdio.h>

void main(void)
{
	int a;	
	unsigned char b;
	
	b = a = 0x12345678;	
	printf("a = %#.8x, b = %#.8x\n", a, b);

	a = b = 0x12345678;	
	printf("a = %#.8x, b = %#.8x\n", a, b);
}
```
## [3-3] 연산자 우선순위 연습
```c
#include <stdio.h>

void main(void)
{
	int a = 10, b = 20, c0, c1, c2, c3, c4;

	c0 = + a - - b;
	c1 = a + b * 2;
	c2 = a * b / 2 % 4;
	c3 = -a * 2 + b / 4;
	c4 = a * ((2 + -b) / 4);
	printf("%d %d %d %d %d\n", c0, c1, c2, c3, c4);
}
```
## [3-4] /, % 연산자의 활용 => 10진수 자리수 분리
```c
#include <stdio.h>

void main(void)
{
	int a = 2345;
	int a4, a3, a2, a1;

	a4 = 
	a3 = 
	a2 = 
	a1 = 

	printf("1000자리=%d, 100자리=%d, 10자리=%d, 1자리=%d\n", a4, a3, a2, a1);
}
```
## [3-5] 가격 절사 판매
```c
#include <stdio.h>

void main(void)
{
	int p = 123456;

	p = 

	printf("%d\n", p);
}
```
## [3-6] 복합대입 연산자
```c
#include <stdio.h>

void main(void)
{
	int a = 20, b = 4;

	a += 3; 
	printf("%d\n", a);

	a -= b;
	printf("%d\n", a);

	a *= b + 2;
	printf("%d\n", a);

	a /= a - b + 1;
	printf("%d\n", a);

	a %= b -= 3;
	printf("%d\n", a);
}
```
## [3-7] 복합대입 연산자의 복원
```c
#include <stdio.h>

void main(void)
{
	int a = 20, b = 4;

	a =
	printf("%d\n", a);

	a =
	printf("%d\n", a);

	a =
	printf("%d\n", a);

	a =
	printf("%d\n", a);

	a =
	printf("%d\n", a);
}
```
## [3-8] ++, -- 증가, 감소 연산자
```c
#include<stdio.h>

void main(void)
{
	int a = 10, b;
	float f = 3.14f;

	a++; 
	f++; 
	printf("%d, %f\n", a, f);

	++a; 
	++f; 
	printf("%d, %f\n", a, f);

	b = ++a;
	printf("a=%d, b=%d\n", a, b);

	b = a++;
	printf("a=%d, b=%d\n", a, b);

	b = ++a + b;
	printf("a=%d, b=%d\n", a, b);

	b = a++ + b;
	printf("a=%d, b=%d\n", a, b);
}
```
## [3-9] ++, --의 side effect
```c
#include<stdio.h>

void main(void)
{
	int a = 10, b = 5;

	a = b++ + b;
	printf("%d, %d\n", a, b);

	printf("%d, %d\n", ++a, ++a);
	printf("%d, %d\n", a++, a++);
}
```
## [3-10] Maximal Munch Rule
```c
#include<stdio.h>

void main(void)
{
	int a = 10, b = 5;

	a = a+++++b;
	printf("%d, %d\n", a, b);
}
```
## [3-11] 16진수의 자리수 분리
```c
#include<stdio.h>

void main(void)
{
	unsigned int x;
	unsigned int x4, x3, x2, x1;

	scanf("%x", &x);

	// 코드 작성

	printf("%X, %X, %X, %X", x4, x3, x2, x1);

}
```
## [3-12] 정수 3개 합과 평균 구하기
```c
#include<stdio.h>

void main(void)
{
	int a, b, c, sum;
	float avg;

	// 코드 작성

	printf("%d, %f\n", sum, avg);
}
```
## [3-13] 다른 타입간 사칙연산
```c
#include<stdio.h>

void main(void)
{
	int ia, ib;
	float fa, fb;
	char ca = 'b', cb = 'B';

	ia = 5 / 3;
	ib = 5 % 3;

	fa = 5 / 3;
	fb = 5.f / 3.f;

	ca = ca + 1;
	cb = cb - 1;

	printf("int   ia = %d, ib = %d\n", ia, ib);
	printf("float fa = %f, fb = %f\n", fa, fb);
	printf("char  ca = %c, cb = %c\n", ca, cb);
}
```
## [3-14] cast 연산자를 이용한 강제 형변환
```c
#include<stdio.h>

void main(void)
{
	int ia, ib;
	float fa, fb;
	char ca = 'b', cb = 'B';

	ia = 5 / 3;
	ib = 5 % 3;

	fa = 5 / 3;
	fb = 5.f / 3.f;

	ca = ca + 1;
	cb = cb - 1;

	printf("int   ia = %d, ib = %d\n", ia, ib);
	printf("float fa = %f, fb = %f\n", fa, fb);
	printf("char  ca = %c, cb = %c\n", ca, cb);
}
```
## [4-1] 함수의 예와 호출
```c
#include <stdio.h>

void no_op(void)
{
}

void welcome(void)
{
	printf("Hello!\n"); 
}

void print_weight(int weight)
{
	printf("Weight = %d\n", weight);
	return;
}

int Get_My_Weight(void)
{
	int weight = 70; 
	return weight;
}

int add(int a, int b)
{
	int c;
	
	c = a + b;
	return c;	
}

void main(void)
{
	int r;
	int x = 50;
	int a = 3;
	int b = 5;

	no_op();
	welcome();
	printf("My Weight = %dkg\n", Get_My_Weight() + 10);
	print_weight(x);
	r = add(a, b);
	printf("add = %d\n", r);
}
```
## [4-2] argument 전달
```c
#include <stdio.h>

int add(int a, int b)
{
	int c;
	
	c = a + b;
	printf("c=%d\n", c);
	return c;	
}

void main(void)
{
	int r;
	int x = 50;
	int a = 3;
	int b = 5;

	printf("add = %d\n", add(3, 5));
	
	printf("add = %d\n", add(a, b));
	
	r = add(x + 2, a);
	printf("add = %d\n", r);
	
	r = add(add(3, 5), add(x, a));
	printf("add = %d\n", r);
}
```
## [4-3] 함수의 위치
```c
#include <stdio.h>

void main(void)
{
	weight(50);
}

void weight(int w)
{
	printf("Weight = %d Kg\n", w);
	return 0;
}
```c
## [4-4] 함수의 선언
```c
#include <stdio.h>

// 여기에 함수 선언

void main(void)
{
	weight(50);
}

void weight(int w)
{
	printf("Weight = %d Kg\n", w);
}
```
## [4-5] 함수의 호출 => 인수의 전달
```c
#include <stdio.h>

void func(char x)
{
	printf("x = %#.8x\n", x);
}

void main(void)
{
	int a = 0x12345678;
	func(a);
}
```
## [4-6] 함수의 호출 => 리턴의 활용 전달
```c
#include <stdio.h>

int add(int a, int b);

void main(void)
{
	int a = 0x12345678;
	int b = 0x87654321;
	unsigned char r;

	r = add(a, b);
	printf("return=%#.8x\n", r);

	add(a, b);
	(void)add(a, b);
}

int add(int a, int b)
{
	return a + b;
}
```
## [4-7] 헤더 파일의 생성
```c
/* [1] weight 함수의 프로토타입을 my.h 파일에 생성한다 */
/* [2] 이 파일을 프로젝트 솔루션으로 불러 온다 */
/* [3] 다음 코드에서 my.h를 include 시킨다 */

#include <stdio.h>
#include "my.h"

void main(void)
{
	weight(50);
}
```
## [4-8] 함수의 분석 연습
```c
#include <stdio.h>

// 사용할 함수들의 선언

void main(void)
{
	printf("sqr=%d\n", sqr(3));
	printf("area=%d\n", area(3, 5));
	printf("arc=%f\n", compute_circle_arc(4.1f));
}

int sqr(int x)
{
	return x * x;
}

int area(int x, int y)
{
	return x * y;
}

float compute_circle_arc(float radius)
{ 
	float pi = 3.141592f;

	radius = 2 * radius * pi;
	return radius;
}
```
## [4-9] 반지름을 입력하면 원의 넓이를 구하는 함수
```c
#include <stdio.h>

float compute_circle_area(float radious);

void main(void)
{
	float r;
	scanf("%f", &r);
	printf("%f\n", compute_circle_area(r));
}

float compute_circle_area(float radious)
{
	float pi = 3.14f;

	// 코드 작성
}
```
## [4-10] float 값의 가장 가까운 정수 값을 넘겨주는 함수
```c
#include <stdio.h>

int find_int(float value);

void main(void)
{
	int r;

	float num;
	scanf("%f", &num);

	r = find_int(num);
	printf("%d\n", r);
}

int find_int(float value)
{
	// 코드 작성
}
```
## [4-11] 차량 5부제 코드 생성
```c
#include <stdio.h>

int make_group(int car);

void main(void)
{
	int car;
	scanf("%d", &car);
	printf("%d\n", make_group(car));
}

int make_group(int car)
{
	// 코드 작성
}
```
## [4-12] 대문자를 소문자로 전환하는 함수 설계
```c
#include <stdio.h>

char Change_Case(char upper)
{
	// 코드 작성	
}

void main(void)
{
	char a;
	
	scanf("%c" , &a );
	printf("%c => %c\n", a, Change_Case(a));
}
```
## [4-13] ASCII 숫자 문자를 정수 숫자로 반환하는 함수
```c
#include <stdio.h>

int Change_Char_to_Int(char num)
{
	// 코드 작성		
}

void main(void)
{
	char a;

	scanf("%c", &a);
	printf("%d\n", Change_Char_to_Int(a));
}
```
## [4-14] 변수의 유효범위
```c
#include <stdio.h>

int a = 1, b = 2, c = 3;

void func(void)
{
	int c = 3000;
	printf("%d %d %d\n", a, b, c);
}

void main(void)
{
	int b = 20, c = 30, d = 40;
	printf("%d %d %d %d\n", a, b, c, d);

	func();

	{
		int c = 300, d = 400;
		printf("%d %d %d %d\n", a, b, c, d);
	}

	{
		int d = -400;
		printf("%d %d %d %d\n", a, b, c, d);
	}
}
```
## [4-15] 스택 분석을 이용한 변수 유효범위의 이해
```c
#include <stdio.h>

int r;

int add(int a, int b)
{
	int r;

	r = a + b;
	return r;
}

void main(void)
{
	int a = 3, b = 4;

	r = add(a, b);
	printf("%d\n", r);
}
```
## [4-16] 손파일링 연습 – 전역변수 은닉
```c
#include <stdio.h>

int a = 10;
int b;
int c = 20;

void f2(void)
{
	int a = 100;

	printf("%d %d %d\n", a, b, c);
}

void f1(void)
{
	int a = 50;
	int b = 500;

	f2();
	printf("%d %d %d\n", a, b, c);
}

void main(void)
{
	int c = 1000;

	f1();
	printf("%d %d %d\n", a, b, c);
}
```
## [4-17] 손파일링 연습 – 지역변수의 유효 범위
```c
#include <stdio.h>

int a = 1;
int b;
int c = 2;

void main(void)
{
	int a = 100;

	{
		int a = 20;
		int b = 10;

		{
			int c = 5;

			printf("%d %d %d\n", a, b, c);
		}

		printf("%d %d %d\n", a, b, c);
	}

	printf("%d %d %d\n", a, b, c);
}
```
## [4-18] 손파일링 연습 – 인수 전달과 리턴
```c
#include <stdio.h>

int a = 1;
int b;
int c = 2;

int f2(int a, int b)
{
	int c = a + b % 2;

	return c * 3;
}

int f1(int a, int x)
{
	int d = 13;

	c = d + a - x;

	return b = f2(b = c + d, a) + 1;
}

void main(void)
{
	int b = 10;
	int x = 3;
	int d = f1(x, a);

	printf("%d %d %d %d\n", a, b, c, d);

	f2(b, a = x + 1);

	printf("%d %d %d %d\n", a, b, c, d);
}
```
## [4-19] #define
```c
#include <stdio.h>

#define MAX 10
#define SQR(x)	x * x

void main(void)
{
	int i;
	int a[MAX];

	for (i = 0; i < MAX; i++)
	{
		a[i] = i;
		printf("%d\n", SQR(a[i]));
	}
}
```
## [4-20] #define 주의 사항
```c
#include <stdio.h>

#define MAX 4;
#define SQR(x)	x * x

void main(void)
{
	int a[MAX] = { 1,2,3,4 };

	printf("%d\n", SQR(5 + 3));
}
```
## [5-1] if 문
```c
#include <stdio.h>

void main(void)
{
	if()	printf("???\n");
	if(1)	printf("True\n");
	if(0)	printf("False\n");
	if(-1)	printf("True\n");
	if(0);	printf("False\n");

	if(0.0)	printf("1\n"); printf("2\n");
	printf("3\n");

	if(0.0) { printf("4\n"); printf("5\n"); }
	printf("6\n");

	if(3.1) { printf("7\n"); printf("8\n"); }
	printf("9\n");
}
```
## [5-2-1] if ~ else 문 1
```c
#include <stdio.h>

void main(void)
{
	if(1)	printf("True\n");
	else	printf("False\n"); 

	if(0)	printf("False\n");
	else	printf("True\n");

	if(1.0)
	{
		printf("1\n");
		printf("2\n");
	}
	else
	{
		printf("3\n");
		printf("4\n");
	}
}
```
## [5-2-2] if ~ else 문 2
```c
#include <stdio.h>

void main(void)
{
	if(0)	printf("1\n");
	else
		if(1) printf("2\n");
		else
			if(2) printf("3\n");
			else  printf("4\n");
}
```
## [5-2-3] if ~ else 문 3
```c
#include <stdio.h>

void main(void)
{
	if(0)	printf("1\n");
	else if(1) printf("2\n");
	else if(2) printf("3\n");
	else  printf("4\n");
}
```
## [5-3] 홀짝을 맞춰라 1
```c
#include <stdio.h>

int Check_Odd_Even(int num)
{
	// 코드 구현
}

void main(void)
{
	int num;
	scanf("%d", &num);
	printf("%d\n", Check_Odd_Even(num));
}
```
## [5-4] 홀짝을 맞춰라 2
```c
#include <stdio.h>

int Check_Odd_Even(int num)
{
	// 코드 구현
}

void main(void)
{
	int num;
	scanf("%d", &num);
	printf("%d\n", Check_Odd_Even(num));
}
```
## [5-5-1] 2,3,5의 배수 판단하기
```c
#include <stdio.h>

int compare(int num)
{
	// 코드 구현
}

void main(void)
{
	int num;
	scanf("%d", &num);
	printf("%d\n", compare(num));
}
```
## [5-5-2] 2,3,5의 배수 판단하기 코드 분석
```c
#include <stdio.h>

int compare(int num)
{
#if 0
	int r = 0;

	if (num % 2 == 0) r = 2;
	else if (num % 3 == 0) r = 3;
	else if (num % 5 == 0) r = 5;
	return r;
#endif

#if 0
	if (num % 2 == 0) return 2;
	else if (num % 3 == 0) return 3;
	else if (num % 5 == 0) return 5;
	else return 0;
#endif

#if 0
	if ((num % 2) == 0) return 2;
	if ((num % 3) == 0) return 3;
	if ((num % 5) == 0) return 5;
	return 0;
#endif

#if 0
	if (!(num % 2)) return 2;
	if (!(num % 3)) return 3;
	if (!(num % 5)) return 5;
	return 0;
#endif
}

void main(void)
{
	int num;
	scanf("%d", &num);
	printf("%d\n", compare(num));
}
```c
## [5-6] 참, 거짓의 결과 값
```c
#include <stdio.h>

void main(void)
{
	int a = 10;
	int b= 0;
	float c = -3.14f;

	if(a) printf("a : True\n");
	if(b) printf("b : True\n");
	if(b == 0) printf("b == 0 : True\n");
	if(b != a) printf("b != a : True\n");
	if(c >= 3.14f) printf("c >= 3.14f : True\n");

	a = b == 1;
	printf("True or False = %d\n", a);

	a = b < 1;
	printf("True or False = %d\n", a);

	a = (c == -3.14f) + (b != 1);
	printf("True or False = %d\n", a);
}
```
## [5-7] 3의 배수 값인지 확인하는 함수
```c
#include <stdio.h>

int multiple_of_3(int num)
{
	// 코드 구현
}

void main(void)
{
	int num;
	scanf("%d", &num);
	printf("%d\n", multiple_of_3(num));
}
```
## [5-8] = 과 ==의 차이
```c
#include <stdio.h>

void main(void)
{
	int a = 0;

	if(a = 3) printf("True\n");
	else printf("False\n");
}
```
## [5-10] 3의 배수 또는 5의 배수 찾기
```c
#include <stdio.h>

int f1(int num)
{
	// 코드 구현
}

void main(void)
{
	int num;
	scanf("%d", &num);
	printf("%d\n", f1(num));
}
```
## [5-11] 4~10 사이 숫자 찾기
```c
#include <stdio.h>

int f1(int num)
{
	// 코드 구현
}

void main(void)
{
	int num;
	scanf("%d", &num);
	printf("%d\n", f1(num));
}
```
## [5-12] 대문자 또는 소문자 찾기
```c
#include <stdio.h>

int f1(char c)
{
	// 구현 
}

void main(void)
{
	char c;
	scanf("%c", &c);
	printf("%d\n", f1(c));
}
```
## [5-13] 조건분기 연산자
```c
#include <stdio.h>

void main(void)
{
	int a = 10;
	int b = 20;
	int c;

	c = if(b < 5) a; else b;
	printf("%d\n", c);
}
```

```c
#include <stdio.h>

void main(void)
{
	int a = 10;
	int b = 20;
	int c;

	c = (b < 5) ? a : b;
	printf("%d\n", c);
}
```
## [5-14] 함수 호출도 수식이다
```c
#include <stdio.h>

void main(void)
{
	int a = 10;

	a ?  printf("True\n") : printf("False\n");
}
```
## [5-15] 주차 요금
```c

// 코드 작성

```
## [5-16] 소문자 f ~ z 찾기
```c
#include <stdio.h>

int func(char c)
{
	// 코드 작성
}

void main(void)
{
	char c;

	scanf("%c", &c);
	printf("%d\n", func(c));
}
```
## [5-17] 대문자 소문자 변경
```c
#include <stdio.h>

char func(char c)
{
	// 코드 작성
}

void main(void)
{
	char c;

	scanf("%c", &c);
	printf("%c\n", func(c));
}
```
## [5-18] L, E, W 찾기
```c
#include <stdio.h>

char func(char c)
{
	// 코드 작성
}

void main(void)
{
	char c;

	scanf("%c", &c);
	printf("%c\n", func(c));
}
```
## [5-19] 수 값에 제일 가까운 정수 값 구하기
```c
#include <stdio.h>

int func(float v)
{
	// 코드 작성	
}

void main(void)
{
	float a;

	scanf("%f", &a);
	printf("%d\n", func(a));
}
```
## [5-20-1] switch ~ case 문의 기본 동작 1
```c
#include <stdio.h>

void main(void)
{
	int a = 2;

	switch (a)
	{
		case 1: printf("1\n");
		case 2: printf("2\n");
		case 3: printf("3\n");
		default: printf("4\n");
	}
}
```
## [5-20-2] switch ~ case 문의 기본 동작 2
```c
#include <stdio.h>

void main(void)
{
	int a = 2;

	switch (a)
	{
		case 1: printf("1\n"); break;
		case 2: printf("2\n"); break;
		case 3: printf("3\n"); break;
		default: printf("4\n");
	}
}
```
## [5-21] 성적 계산 함수
```c
#include <stdio.h>

// 함수 func 설계

void main(void)
{
	int score;

	scanf("%d", &score);
	printf("%c\n", func(score));
}
```
## [6-2] 0 부터 입력 받은 수 까지 짝수를 인쇄하는 코드

```c

// 코드 작성

```
## [6-3] 입력 받은 두 수 사이의 3의 배수를 인쇄하는 코드

```c

// 코드 작성

```
## [6-4] *을 입력 받은 수 만큼 인쇄하는 코드


```c

// 코드 작성

```
## [6-5] 숫자를 7 부터 입력 받은 개수 만큼 연속 인쇄하는 코드

```c

// 코드 작성

```
## [6-6] ‘A’부터 입력 받은 알파벳까지 알파벳을 인쇄 

```c

// 코드 작성

```
## [6-7] ‘D’부터 입력 받은 알파벳 사이 글자를 2개씩 건너 띄며 인쇄

```c

// 코드 작성

```
## [6-8] 3,6,9 게임

```c

// 코드 작성

```
## [6-9] 정수의 자리수 구하기

```c

// 코드 작성

```
## [6-10] 정수의 자리수의 합 구하기
```c

// 코드 작성

```
## [6-11-1] 사각별 찍기 1
```c
#include <stdio.h>

void main(void)
{
	int i, j;

	for (i = 0; i < 5; i++)
		for (j = 0; j < 5; j++)
			printf("*");
	printf("\n");
}
```
## [6-11-2] 사각별 찍기 2
```c
#include <stdio.h>

void main(void)
{
	int i, j;

	for (i = 0; i < 5; i++)
	{
		for (j = 0; j < 5; j++)
		{
			printf("*");
		}
		printf("\n");
	}
}
```
## [6-12-1] 별 자판기 - 삼각별
```c

// 코드 작성

```
## [6-12-2] 별 자판기 - 역삼각별
```c

// 코드 작성

```
## [6-12-3] 별 자판기 - 반대 삼각별
```c

// 코드 작성

```
## [6-12-4] 별 자판기 - 반대 역삼각별
```c

// 코드 작성

```
## [6-12-5] 별 자판기 - 트리별
```c

// 코드 작성

```
## [6-13] 구구단 인쇄
```c

// 각 단의 구분은 아래 코드를 이용한다
// printf("=======================\n");

// 코드 작성

```
## [6-14] break의 동작
```c
#include <stdio.h>

void main(void)
{
	int i;

	for (i = 0; i < 10; i++)
	{
		if (i == 7) break;
		printf("%d\n", i);
	}
}
```
## [6-15] continue의 동작
```c
#include <stdio.h>

void main(void)
{
	int i;

	for (i = 0; i < 10; i++)
	{
		if (i == 7) break;
		if (i % 3) continue;
		printf("%d\n", i);
	}
}
```
## [6-16] break의 for 루프 탈출
```c
#include <stdio.h>

void main(void)
{
	int i, j;

	for (i = 0; i < 20; i++)
	{
		for (j = 0; j < 10; i++, j++)
		{
			if (j == 4) break;
			printf("%d %d\n", i, j);
		}

		if (i % 3) continue;
	}
}
```
## [6-17] j == 4 일 때 완전히 루프를 탈출하려면?
```c

// 코드 작성

```
## [6-18-1] 다중 루프의 탈출 : flag 이용
```c
#include <stdio.h>

void main(void)
{
	int i, j, flag = 0;

	for (i = 0; i < 20; i++)
	{
		for (j = 0; j < 10; i++, j++)
		{
			if (j == 4)
			{
				flag = 1;
				break;
			}
			printf("%d %d\n", i, j);
		}

		if (flag != 0) break;
		if (i % 3) continue;
	}

	printf("EXIT\n");
}
```
## [6-18-2] 다중 루프의 탈출 : goto문 이용
```c
#include <stdio.h>

void main(void)
{
	int i, j, flag = 0;

	for (i = 0; i < 20; i++)
	{
		for (j = 0; j < 10; i++, j++)
		{
			if (j == 4) goto TAG1;
			printf("%d %d\n", i, j);
		}

		if (i % 3) continue;
	}

TAG1:
	printf("EXIT\n");
}
```
## [6-19] 짝수와 3의 배수를 제외한 숫자 인쇄
```c
// 숫자의 인쇄는 아래 코드를 이용한다
// printf("%3d ", i);
#include <stdio.h>

void func(int num)
{
	// 코드 구현
}

void main(void)
{
	int n;

	scanf("%d", &n);
	func(n);
}
```
## [6-20] 1부터 입력 값까지 소수를 모두 인쇄하는 함수
```c

// 코드 작성

```
## [6-22-1] 알아두면 편리한 while 구문 1

```c
#include <stdio.h>

void main(void)
{
	int a = 0;

	while (a < 10)
	{
		printf("%d\n", a);
		a++;
	}
}
```
## [6-22-2] 알아두면 편리한 while 구문 2
```c
#include <stdio.h>

void main(void)
{
	int a = 0;

	while (!(a == 13))
	{
		printf("%d\n", a);
		a++;
	}
}
```
## [6-23] 받은 수부터 0까지 3의 배수를 인쇄하는 함수

```c

// 코드 작성

```
## [6-24] X가 입력될 때까지 입력 받기

```c

// 코드 작성

```
## [6-25] do ~ while의 일반적인 형식
```c
#include <stdio.h>

void main(void)
{
	int a = 0;

	do a++; while (a < 10);

	a = 10;

	do
		a++;
	while (a < 10);

	a = 10;

	do
	{
		a++;
	} while (a < 10);

	printf("a=%d\n", a);
}
```
## [6-26-1] Factoral - for 이용
```c
#include <stdio.h>

unsigned long long int Factorial(int num)
{
	// for 이용 코드 작성
}

void main(void)
{
	int value;

	scanf("%d", &value);
	printf("%llu\n", Factorial(value));
}
```
## [6-26-2] Factoral - while 이용

```c
#include <stdio.h>

unsigned long long int Factorial(int num)
{
	// while 이용 코드 작성
}

void main(void)
{
	int value;

	scanf("%d", &value);
	printf("%llu\n", Factorial(value));
}
```
## [6-27] 중간값 찾기

```c

// 코드 작성

```
## [7-1] 배열의 메모리 분석

```c
#include <stdio.h>

void main(void)
{
	int a[4];
	
	a[0] = 0;
	a[1] = 10;
	a[2] = 20;
	a[3] = 30;

	printf("%p %p %p %p %p\n", &a, &a[0], &a[1], &a[2], &a[3]);
	printf("%d %d %d %d\n", a[0], a[1], a[2], a[3]);
}
```
## [7-2-1] 배열의 선언과 초기화 - 초과 저장

```c
#include <stdio.h>

void main(void)
{
	int a[4] = { 10, 20, 30, 40, 50 };
	char b[3] = "ABCD";
	printf("%s\n", b);
}
```
## [7-2-2] 배열의 선언과 초기화 - 요소수 미지정

```c
#include <stdio.h>

void main(void)
{
	int a[] = { 10, 20, 30, 40, 50 };
	char b[] = "ABCD";
	printf("%s\n", b);
}
```
## [7-3] 암기왕

```c
#include <stdio.h>

void main(void)
{
	int a[10];

	// 코드 구현
}
```
## [7-4] 암기왕 => 10개 버전

```c

// 코드 작성

```
## [7-5-1] 암기왕 코드 분석

```c
#include <stdio.h>

void main(void)
{
	int i;
	int a[5];

	for(i = 0; i < 5; i++)
	{
		scanf("%d", &a[i]);
	}

	for(i = 0; i < 5; i++)
	{
		printf("%d\n", a[i]);
	}
}
```
## [7-5-2] 암기왕 10개 받기 코드 수정

```c
#include <stdio.h>

#define ARR_MAX  10

void main(void)
{
	int i;
	int a[ARR_MAX];

	for (i = 0; i < ARR_MAX; i++)
	{
		scanf("%d", &a[i]);
	}

	for (i = 0; i < ARR_MAX; i++)
	{
		printf("%d\n", a[i]);
	}
}
```
## [7-6] 행운권 추첨

```c

// 코드 작성

```
## [7-7] 대문자의 개수

```c

// 코드 작성

```
## [7-8] 알밤만 담는 바구니

```c

// 코드 작성

```
## [7-9] 가변 개수 정수 입력 받기

```c
#include <stdio.h>

void main(void)
{
	int i, n;
	int a[100 + 2];

	scanf("%d", &n);

	for(i = 0; i < n; i++)
	{
		scanf("%d", &a[i]);
	}

	for (i = 0; i < n; i++)
	{
		printf("%d ", a[i]);
	}
}
```
## [7-10] 귤 판매

```c

// 코드 작성

```
## [7-11] 알밤을 분류하여 담는 바구니

```c

// 코드 작성

```
## [7-12] 키 순서대로 집합

```c

// 코드 작성

```
## [7-13] 암호화 프로그램
```c

// 코드 작성

```
## [7-14] 복호화 프로그램

```c

// 코드 작성

```
## [7-15] 성적처리용 수퍼 컴퓨터

```c

// 코드 작성

```
## [7-16] 문자열 비교

```c
#include <stdio.h>

void main(void)
{
	char a[11];
	char b[11];

	scanf(" %s", a);
	scanf(" %s", b);

	// 코드 구현
}
```
## [7-17] 이차원 배열 구조와 초기화

```c
#include <stdio.h>

void main(void)
{
	int i;
	int a[4][4] = { {1,2,3,4}, {5,6,7,8}, {9,10,11,12}, {13,14,15,16} };
	int sum[2] = { 0, };

	for (i = 0; i < 4; i++)
	{
		sum[0] += a[i][i];
		sum[1] += a[i][3 - i];
	}
	printf("%d %d", sum[0], sum[1]);
}
```
## [7-18] 이차원 배열 메모리 구조, 요소수

```c
#include <stdio.h>

#define ARR_SIZE(x) (sizeof((x))/sizeof((x)[0]))

void main(void)
{
	int a[3][4] = { {1,2,3,4}, {5,6,7,8}, {9,10,11,12} };

	printf("%d, %d\n", ARR_SIZE(a), ARR_SIZE(a[0]));
	printf("%p, %p, %p, %p\n", &a,&a[0],&a[0][0],&a[1]);
}
```
## [7-19] 2차원 배열로 정수 입력 받아서 가장 큰 값 인쇄

```c
#include <stdio.h>

int a[5][5];

void input(void)
{
	int i, j;

	for (i = 0; i < 5; i++)
	{
		for (j = 0; j < 5; j++)
		{
			scanf("%d", &a[i][j]);
		}
	}
}

void main(void)
{
	int i, j;

	input();

	// 코드 구현
}
```
## [7-20] 가장 작은 값의 행과 열 번호 찾기

```c

// 코드 작성

```
## [7-21] 합이 가장 큰 행과 열 찾기

```c

// 코드 작성

```
## [7-22] 이차원 배열 Transpose 

```c
#include <stdio.h>

int a[4][4] = { {1,2,3,4}, {5,6,7,8}, {9,10,11,12}, {13, 14, 15, 16} };
int b[4][4];

void transpose1(void)
{
	// 코드 구현
}

void main(void)
{
	int i, j;

	for (i = 0; i < 4; i++)
	{
		for (j = 0; j < 4; j++)
		{
			printf("%d ", a[i][j]);
		}
		printf("\n");
	}

	transpose1();

	for (i = 0; i < 4; i++)
	{
		for (j = 0; j < 4; j++)
		{
			printf("%d ", b[i][j]);
		}
		printf("\n");
	}
}
```
## [7-23] 다른 모양의 이차원 배열 Transpose 

```c
#include <stdio.h>

int a[3][4] = { {1,2,3,4}, {5,6,7,8}, {9,10,11,12} };
int b[4][3];

void transpose2(void)
{
	// 코드 구현
}

void main(void)
{
	int i, j;

	for (i = 0; i < 3; i++)
	{
		for (j = 0; j < 4; j++)
		{
			printf("%d ", a[i][j]);
		}
		printf("\n");
	}

	transpose2();

	for (i = 0; i < 4; i++)
	{
		for (j = 0; j < 3; j++)
		{
			printf("%d ", b[i][j]);
		}
		printf("\n");
	}
}
```
## [7-24] 문자열을 저장하는 배열

```c
#include <stdio.h>

void main(void)
{
	int i;
	char s[3][11] = { "Hello", "C", "World!" };

	for (i = 0; i < 3; i++)
	{
		printf("%c : %s\n", s[i][0], s[i]);
	}
}
```
## [7-25-1] 문자열 3개 입력 받기

```c
#include <stdio.h>

void main(void)
{
	int i;
	char a[3][21];

	for (i = 0; i < 3; i++)
	{
		scanf(" %s", &a[i]);
	}

	for (i = 0; i < 3; i++)
	{
		printf("%s ", a[i]);
	}
}
```
## [7-25-2] 공백이 포함된 문자열 3개 입력 받기

```c
#include <stdio.h>

void main(void)
{
	int i;
	char a[3][21];

	for (i = 0; i < 3; i++)
	{
		gets(&a[i]);
	}

	for (i = 0; i < 3; i++)
	{
		printf("%s ", a[i]);
	}
}
```
## [7-26] 사람 찾기

```c

// 코드 작성

```
## [7-27] 가위 바위 보 게임

```c

// 코드 작성

```
## [7-28] srand를 추가한 가위 바위 보 게임

```c

// 코드 작성

```
## [8-1] 구조체 템플릿 선언과 멤버 액세스

```c
#include <stdio.h>

void main(void)
{
	struct st
	{
		int a;
		char b;
	};

	struct st x;

	x.a = 200;
	x.b = 'B';
	printf("x.a = %d, x.b = %c\n", x.a, x.b);
}
```
## [8-2] 다양한 구조체 멤버

```c
#include <stdio.h>

struct st1
{
	int a;
	char b;
};

struct st2
{
	int c;
	int d[4];
	struct st1 e;
};

void main(void)
{
	struct st2 x = { 1, {10,20,30,40}, {100, 'A'} };

	printf("%d %d %d\n", x.c, x.d[0], x.d[1]);
	printf("%d %c\n", x.e.a, x.e.b);
}
```
## [8-3-1] 구조체는 기본형 타입 1

```c
#include <stdio.h>

void main(void)
{
	int a, b = 10;

	a = b;
	printf("%d, %d\n", a, b);
}
```c
## [8-3-2] 구조체는 기본형 타입 2

```c
#include <stdio.h>

void main(void)
{
	struct st
	{
		int a;
		char b;
	}x, y, z = { 100, 'A' };

	x.a = z.a;
	x.b = z.b;

	y = z;

	printf("%d, %d\n", x.a, x.b);
	printf("%d, %d\n", y.a, y.b);
}
```
## [8-4] 데이터 멤버는 멤버의 타입

```c
#include <stdio.h>

struct st
{
	int a;
	char b[4];
}x = { 100, "ABC" };

void main(void)
{
	char a[4] = "ABC";

	a = "LEW";
	x.b = "LEW";
}
```
## [8-5] 문자열을 복사 또는 메모리를 복사

```c
#include <stdio.h>
#include <string.h>

struct st
{
	int a;
	char b[4];
}x = { 100, "ABC" };

void main(void)
{
	char a[4] = "ABC";

	memcpy(a, "LEW", sizeof("LEW"));
	strcpy(x.b, "LEW");

	printf("%s, %s\n", a, x.b);
}
```
## [8-6] 구조체 배열

```c
#include <stdio.h>

struct st
{
	int a;
	char b;
};

void main(void)
{
	int i;
	struct st x[4] = { {10, 'A'}, {20, 'B'}, {30, 'C'}, {40, 'D'} };

	for (i = 0; i < sizeof(x) / sizeof(x[0]); i++)
	{
		x[i].a = i;
		printf("%d, %c\n", x[i].a, x[i].b);
	}
}
```
## [8-7] 공용체

```c
#include <stdio.h>

void main(void)
{
	union uni
	{
		int a;
		unsigned char b;
	} x = { 0x12345678 };

	printf("0x%x, 0x%x\n", x.a, x.b);
	printf("0x%.8x, 0x%.8x\n", &x.a, &x.b);
	printf("%d, %d\n", sizeof(x.a), sizeof(x.b));
	printf("0x%.8x, %d\n", &x, sizeof(x));

	x.b = 0xEF;
	printf("0x%x, 0x%x\n", x.a, x.b);
}
```
## [8-8] 공용체 활용 예 : 엔디안 모드 변경

```c
#include <stdio.h>

union uni
{
	int a;
	char b[4];
};

int Change_Endian(int data)
{
	char tmp;
	union uni x;
	x.a = data;

	// 코드 작성

	return x.a;
}

void main(void)
{
	int a = 0x12345678;

	printf("0x%.8x => 0x%.8x\n", a, Change_Endian(a));
}
```
## [8-9] typedef

```c
#include <stdio.h>

typedef signed int SI;
typedef unsigned char BYTE;

void main(void)
{
	SI a = 100;
	BYTE x[4] = { 'A','B','C','D' };

	printf("%d, %c, %c\n", a, x[0], x[1]);
}
```
## [8-10] 구조체 및 공용체의 typedef 방법

```c
#include <stdio.h>

typedef struct st
{
	int a;
	char b;
}ST1;

void main(void)
{
	ST1 x = { 100, 'A' };

	printf("%d, %c\n", x.a, x.b);
}
```
## [9-1] 포인터

```c
#include <stdio.h>

void main(void)
{
	int a = 10;
	int * p = &a;

	printf("0x%p 0x%p %d %d\n", &a, p, a, *p);
	printf("%d %d\n", sizeof(p), sizeof(*p));
}
```
## [9-2] 다양한 타입을 가리키는 포인터

```c
#include <stdio.h>

void main(void)
{
	char a = 'A';
	char *p = &a;

	double f = 3.14;
	double *q = &f;

	printf("%d, %c\n", sizeof(*p), *p);
	printf("%d, %f\n", sizeof(*q), *q);
	printf("0x%p, 0x%p\n", p, p + 1);
	printf("0x%p, 0x%p\n", q, q + 1);
}
```
## [9-3] Call by Value, Call by Address

```c
#include <stdio.h>

void f1(int b)
{
	b = 100;
	printf("%d\n", b);
}

void f2(int *p)
{
	*p = 100;
	printf("%d\n", *p);
}

void main(void)
{
	int a = 10;

	f1(a);
	printf("%d\n", a);

	f2(&a);
	printf("%d\n", a);
}
```
## [9-4] %s 포맷 지시자와 문자열

```c
#include <stdio.h>

void main(void)
{
	char a[] = "Hello";
	char *p = "Hello";

	printf("%s\n", "Hello");
	printf("%s, %s, %s\n", &a[0], a, p);
	printf("%s, %s, %s\n", "Hello" + 1, a + 1, p + 1);
}
```
## [9-5] 문자열의 정체

```c
#include <stdio.h>

char * func(char * q)
{
	printf("%s, %c, %c\n", q, q[0], q[1]);
	printf("0x%p, 0x%p, %c, %c\n", q, q + 1, *q, *(q + 1));

	return q + 2;
}

void main(void)
{
	char *p = "Hello";

	printf("%s, 0x%p, 0x%p\n", "Hello", "Hello", "Hello" + 1);
	printf("%c, %c, %c, %c\n", "Hello"[0], "Hello"[1], *"Hello", *("Hello" + 1));
	printf("%s\n", func("Hello"));
}
```
## [9-6-1] *p++, *++p의 동작

```c
#include <stdio.h>

void main(void)
{
	int cnt = 0;
	char *p = "Embedded";

	while (*p)
	{
		if (*p++ == 'd') cnt++;
	}

	printf("%d\n", cnt);
}
```
## [9-6-2] [] 연산자를 사용한 코드

```c
#include <stdio.h>

void main(void)
{
	int cnt = 0, i = 0;
	char *p = "Embedded";

	while (p[i])
	{
		if (p[i++] == 'd') cnt++;
	}

	printf("%d\n", cnt);
}
```
## [9-7] 문자열 복사

```c
#include <stdio.h>

void str_copy1(char * d, char * s)
{
	int i;

	for (i = 0; ; i++)
	{
		d[i] = s[i];
		if (d[i] == '\0') return;
	}
}

void str_copy2(char * d, char * s)
{
	while (*d++ = *s++);
}

void main(void)
{
	char a[5], b[5];
	char c[5] = "ABCD";

	str_copy1(a, c);
	str_copy2(b, c);
	printf("%s %s %s\n", a, b, c);
}
```
## [9-8] 문자열 길이 측정

```c
#include <stdio.h>

unsigned int str_length(char * d)
{
	// 코드 작성

}

void main(void)
{
	char a[] = "Willtek";

	printf("%d\n", sizeof(a));
	printf("%d\n", str_length(a));
}
```
## [9-9] 문자열 연결

```c
#include <stdio.h>

void str_add(char * d, char * s)
{
	// 코드 작성

}

void main(void)
{
	char a[15] = "Willtek";
	char b[15] = " Corp.";

	str_add(a, b);

	printf("%s\n", a);
}
```
## [9-10] 문자열 비교

```c
#include <stdio.h>

int str_comp(char *a, char *b)
{
	// 코드 작성

}

void main(void)
{
	printf("%d\n", str_comp("ABC", "BC"));
	printf("%d\n", str_comp("ABC", "AC"));
	printf("%d\n", str_comp("ABC", "AB"));
	printf("%d\n", str_comp("abc", "ABC"));
	printf("%d\n", str_comp("ab", " "));
	printf("%d\n", str_comp("A", "AB"));
}
```
## [9-11] 10개 정수를 갖는 배열의 합을 구하는 함수

```c
#include <stdio.h>

int sum1(int a[10])
{
	int i, s = 0;

	for (i = 0; i < 10; i++)
	{
		s += a[i];
	}

	return s;
}

int sum2(int a[10])
{
	int i, s = 0;

	for (i = 0; i < sizeof(a) / sizeof(a[0]); i++)
	{
		s += a[i];
	}

	return s;
}

int sum3(int *a)
{
	int i, s = 0;

	for (i = 0; i < sizeof(a) / sizeof(a[0]); i++)
	{
		s += a[i];
	}

	return s;
}

void main(void)
{
	int a[10] = { 1,2,3,4,5,6,7,8,9,10 };
	int r;

	r = sum1(a);
	printf("SUM1 = %d\n", r);

	r = sum2(a);
	printf("SUM2 = %d\n", r);
	
	r = sum3(a);
	printf("SUM3 = %d\n", r);	
}
```
## [9-12] 배열 활용식을 이용한 요소 액세스

```c
#include <stdio.h>

void main(void)
{
	int a[4] = { 1,2,3,4 };

	printf("%d\n", a[0]);
	printf("%d\n", a[3]);
	printf("%d\n", a[4]);
	printf("%d\n", a[-1]);

	printf("%d\n", (a + 1)[2]);
	printf("%d\n", a[3]);
}
```
## [9-13] 포인터의 [] 연산자 사용

```c
#include <stdio.h>

void main(void)
{
	int a[4] = { 1,2,3,4 };
	int *p = a;

	printf("%d, %d\n", a[0], *p);
	printf("%d, %d\n", a[1], *(p + 1));
}
```
## [9-14] 함수의 배열 Parameter

```c
#include <stdio.h>

void func()
{
	printf("a[3] = %d\n", );
}

void main(void)
{
	int a[4] = { 1,2,3,4 };
	func(a);
}
```
## [9-15] 함수의 배열 Return

```c
#include <stdio.h>

func(void)
{
	static int a[4] = { 1,2,3,4 };
	return a;
}

void main(void)
{
	printf("a[3] = %d\n", func();
}
```
## [9-16] 대치법의 이해

```c
#include <stdio.h>

int x[4] = { 1,2,3,4 };

int *f1(void)
{
	return x;
}

void f2(int *p)
{
	printf("%d, %d, %d, %d\n", x[2], *(x + 2), p[0], *p);
}

void main(void)
{
	int *p;
	int *a[4] = { x + 3, x + 2, x + 1, x };

	p = x;

	printf("%d, %d\n", x[2], p[2]);
	printf("%d, %d, %d, %d\n", x[2], *(x + 2), a[3][2], *a[1]);
	printf("%d, %d, %d, %d\n", x[2], *(x + 2), f1()[2], *(f1() + 2));
	f2(x + 2);
}
```
## [9-17] 포인터가 가리키는 대상

```c
#include <stdio.h>

void main(void)
{
	int a = 100;
	int b[4] = {10, 20, 30, 40};
	int c[2][3] = {{11,22,33},{44,55,66}};

	int *p = &a;
	int (*q)[4] = &b;
	int (*r)[2][3] = &c;

	printf("%d, %d, %d\n",  *p,  (*q)[3], (*r)[1][2]);
	printf("%d, %d, %d\n", p[0], q[0][3], r[0][1][2]);
}
```
## [9-18] 구조체 포인터

```c
#include <stdio.h>

struct st
{
	int a;
	char b;
}x = { 10, 'A' };

void main(void)
{
	struct st * p = &x;

	// 코드 작성

	printf("%c\n", x.b);
}
```
## [9-19] 구조체 포인터를 전문으로 취하는 연산자
```c
#include <stdio.h>

struct st
{
	int a;
	char b;
}x = { 10, 'A' };

void main(void)
{
	struct st * p = &x;

	(*p).b = 'L';
	printf("%c\n", x.b);

	p->b = 'K';
	printf("%c\n", x.b);

	p[0].b = 'L';
	printf("%c\n", x.b);
}
```
## [9-20] 구조체의 함수 전달

```c
#include <stdio.h>

struct st
{
	int num;
	char name[10];
	int score;
};

void cheat(struct st math)
{
	math.score = 100;
}

void main(void)
{
	struct st math = { 1, "KIM", 10 };

	cheat(math);
	printf("%s: %d점\n", math.name, math.score);
}
```
## [9-21] 구조체 포인터 활용

```c
#include <stdio.h>

struct st
{
	int num;
	char name[10];
	int score;
};

void cheat(struct st * math)
{
	// 코드 작성
}

void main(void)
{
	struct st math = { 1, "KIM", 10 };

	cheat(&math);
	printf("%s: %d점\n", math.name, math.score);
}
```
## [9-22] 구조체 배열의 함수 전달

```c
#include <stdio.h>

struct st
{
	int num;
	char name[10];
	int score;
};

void cheat1(struct st * p)
{
	// 코드 작성
}

void cheat2(struct st * p)
{
	// 코드 작성
}

void main(void)
{
	struct st math[4] = { {1,"LEW",10}, {2,"KIM",20}, {3,"SONG",30}, {4,"MOON",40} };

	cheat1(&math[1]);
	printf("%s: %d점\n", math[1].name, math[1].score);

	cheat2(math);
	printf("%s: %d점\n", math[1].name, math[1].score);
}

```
## [9-23-1] 가변 크기 동적 배열 생성 1
```c
#include <stdio.h>
#include <stdlib.h>

void main(void)
{
	int i;
	int * p;

	p = malloc(40);

	for (i = 0; i < 10; i++)
	{
		*(p + i) = i;
	}

	for (i = 0; i < 10; i++)
	{
		printf("%d\n", *(p + i));
	}
}
```
## [9-23-2] 가변 크기 동적 배열 생성 2

```c
#include <stdio.h>
#include <stdlib.h>

void main(void)
{
	int i;
	int * p;

	p = malloc(40);

	for (i = 0; i < 10; i++)
	{
		p[i] = i;
	}

	for (i = 0; i < 10; i++)
	{
		printf("%d\n", p[i]);
	}
}
```
## [9-24] void *

```c
#include <stdio.h>

int main(void)
{
	int i = 10;
	char c = 'a';
	
	int *p = &i;
	char *q = &c;
	void * r;

	p = r = q;
	printf("%c\n", *p);

	q = (void *)0;
}
```
## [9-25] free

```c
#include <stdio.h>

int main(void)
{
	int *p = malloc(8 * sizeof(int));
	char * q = malloc(10 * sizeof(char));
	void * r = q;
	
	free(p);
	free(r);
}
```
## [9-26] malloc과 calloc의 차이

```c
#include <stdio.h>
#include <stdlib.h>

void main(void)
{
	int i;
	int * p;

	p = malloc(10 * sizeof(int));

	if (p == 0x0) return;

	for (i = 0; i < 10; i++)
	{
		printf("malloc[%d]=%d\n", i, p[i]);
	}

	free(p);

	printf("\n\n");

	p = calloc(10, sizeof(int));

	if (p == 0x0) return;

	for (i = 0; i < 10; i++)
	{
		printf("calloc[%d]=%d\n", i, p[i]);
	}

	free(p);
}
```
## [9-27] realloc의 동작

```c
#include <stdio.h>
#include <stdlib.h>

void main(void)
{
	int i;
	int * p;

	p = malloc(5 * sizeof(int));
	if (p == 0x0) return;

	for (i = 0; i < 5; i++)
	{
		p[i] = i;
	}

	p = realloc(p, 10 * sizeof(int));
	if (p == 0x0) return;

	for (i = 5; i < 10; i++)
	{
		p[i] = i;
	}

	for (i = 0; i < 10; i++)
	{
		printf("[%d]=%d\n", i, p[i]);
	}

	realloc(p, 0);
}
```
