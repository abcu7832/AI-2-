#include "device_driver.h"

#define LCDW			(320)
#define LCDH			(240)
#define X_MIN	 		(0)
#define X_MAX	 		(LCDW - 1)
#define Y_MIN	 		(0)
#define Y_MAX	 		(LCDH - 1)

#define FROG_STEP		(5)
#define FROG_SIZE_X		(10)
#define FROG_SIZE_Y		(10)
#define FROG_COLOR		GREEN
#define BACK_COLOR		BLACK
#define SNAKE_COLOR     CYAN
#define FLY_COLOR       PURPLE

#define FLY_STEP		(2)
#define FLY_SIZE_X		(5)
#define FLY_SIZE_Y		(5)

#define GAME_OVER		(1)

#define MAZE_CELL_SIZE 	(20)  // 미로 셀 크기 (20x20)
#define MAZE_ROWS 		(LCDH / MAZE_CELL_SIZE)  // 12행
#define MAZE_COLS 		(LCDW / MAZE_CELL_SIZE)  // 16열
#define MAX_EMPTY_CELLS (20)  // 적절한 크기로 조정

#define DIPLAY_MODE		3

typedef struct{
	int x,y;//위치
	int w,h;//너비, 높이
	int ci;//색
	int dir;//방향 or 배치상태
}QUERY_DRAW;

static QUERY_DRAW snake[2], fly, poison[4], human;

typedef struct{
	int x,y;//위치
	int w,h;//너비, 높이
	int ci;//색
	int dir;//방향
    int stop;//쥐약먹은 상태
}FROGs;

static FROGs frog;

typedef struct {
    int x, y;
    int dir; // 0:상, 1:하, 2:좌, 3:우
    int active;
    int speed;
    int distance; // 이동한 누적 거리
} Projectile;

static Projectile projectile; // 전역 발사체 객체

static int fly_CNT;
static int empty_cells[MAX_EMPTY_CELLS][2];
static int empty_cell_count = 0;

static int snake_stopped[2] = {0, 0};
static int snake_stop_counter[2] = {0, 0};

static unsigned int rand_seed = 0;

static int human_stopped = 0;
static int human_stop_counter = 0;

static int level;
static int eat_poison;
static int dest_x, dest_y;
// 미로 데이터 (1: 벽, 0: 길)

uint8_t maze[MAZE_ROWS][MAZE_COLS] = 
{// 0: 길, 1: 벽
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
    {1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1},
    {1,0,1,1,1,0,0,0,0,0,0,1,1,1,0,1},
    {1,0,0,0,1,0,1,0,1,1,0,0,0,1,0,1},
    {1,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1},
    {1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1},
    {1,0,1,1,1,1,0,1,1,1,0,1,1,1,0,1},
    {1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1},
    {1,0,1,0,1,1,1,0,1,0,1,1,0,1,0,1},
    {1,0,1,0,0,0,0,0,1,0,1,1,0,1,0,1},
    {1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1},
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1}
};

extern volatile int TIM4_expired;
extern volatile int USART1_rx_ready;
extern volatile int USART1_rx_data;
extern volatile int Jog_key_in;
extern volatile int Jog_key;
extern volatile int song_on;
extern volatile int SysTick_Flag;
extern volatile int start;
extern volatile int TIM4_expired;
extern volatile int Jog_key_in;
extern volatile int Jog_key;
extern tImage frog_gameover;
extern tImage frog_gameclear;

void LCD_INITIAL_Display(void);//초기 LCD화면
static int Check_Wall_Collision(int new_x, int new_y, int w, int h);// 새 위치가 미로 벽과 겹치는지 확인
static int Check_Collision(FROGs * obj1, QUERY_DRAW * obj2);// 두 obj 사이에 충돌이 발생했는지 확인하는 함수
static void k0(void);// UP(0)
static void k1(void);// DOWN(1)
static void k2(void);// LEFT(2)
static void k3(void);// RIGHT(3)
static void Init_Projectile(void);
static void Fire_Net(int dir);
static void Update_Projectile(void);
static int Frog_Move(int k);//개구리 움직임 
static void Fly_Move(void);//파리 움직임 
static int Snake_Move(void);//뱀 움직임 
static void Place_Poison(int poison_index);//독 배치
static int Human_Move(void);//인간 움직임
void Game_Init(void);//게임 초기 세팅
void LCD_GAMEOVER_Display(void);//gameover LCD화면
void LCD_GAMECLEAR_Display(void);//gameclear LCD화면
void GAMEOVER_func(void);//게임오버함수
void GAMECLEAR_func(void);//게임클리어함수

void System_Init(void)
{
	Clock_Init();
	LED_Init();
	Key_Poll_Init();
	Uart1_Init(115200);

	SCB->VTOR = 0x08003000;
	SCB->SHCSR = 7<<16;
}

void Main(void)
{
	System_Init();
	Uart_Printf("Game Project\n");

	NVIC_SetPriorityGrouping(3); 	// Binary Point = 4 (Group = 16)
	NVIC_SetPriority(30, 1); 		// TIM4
	NVIC_SetPriority(37, 2); 		// USART1
	NVIC_SetPriority(23, 3); 		// EXTI9_5
	
	Lcd_Init(DIPLAY_MODE);
	Jog_Poll_Init();
	Jog_ISR_Enable(1);

	int fly_reset_tim = 0;
	// TIM3 PWM 초기화 (CNT 초기화 추가)
    TIM3_Out_Init();
	
	for(;;)
	{        
        LCD_INITIAL_Display(); // 초기 화면 표시
        Game_Init();
		TIM4_Repeat_Interrupt_Enable(1, 10);//10ms
        SysTick_OS_Tick(100);//100ms마다 timeout
    
		for(;;)//IN GAME
		{
			switch(fly_CNT){
				case 1: Lcd_Draw_Box((16*MAZE_CELL_SIZE - 5), (11*MAZE_CELL_SIZE + 5), 5, 10, PURPLE); break;
				case 2: Lcd_Draw_Box((16*MAZE_CELL_SIZE - 10), (11*MAZE_CELL_SIZE + 5), 5, 10, PURPLE); break;
				case 3: Lcd_Draw_Box((16*MAZE_CELL_SIZE - 15), (11*MAZE_CELL_SIZE + 5), 5, 10, PURPLE); break;
				case 4: Lcd_Draw_Box((16*MAZE_CELL_SIZE - 20), (11*MAZE_CELL_SIZE + 5), 5, 10, PURPLE); break;
				case 5: Lcd_Draw_Box((16*MAZE_CELL_SIZE - 25), (11*MAZE_CELL_SIZE + 5), 5, 10, PURPLE); break;
				case 6: Lcd_Draw_Box((16*MAZE_CELL_SIZE - 30), (11*MAZE_CELL_SIZE + 5), 5, 10, PURPLE); break;
				case 7: Lcd_Draw_Box((16*MAZE_CELL_SIZE - 35), (11*MAZE_CELL_SIZE + 5), 5, 10, PURPLE); break;
                default: Lcd_Draw_Box((16*MAZE_CELL_SIZE - 40), (11*MAZE_CELL_SIZE + 5), 35, 10, BLACK);
			}
			int game_over = 0;
            int game_clear = 0;
            static int last_dir = -1; // 마지막 이동 방향 저장

            if(eat_poison == 4)
            {
                game_over = 1;
            }

			if(Jog_key_in) 
			{
                if((Jog_key >= 0) && (Jog_key <=3)) { last_dir = Jog_key; }
                
                if((Jog_key == 5) && (last_dir != -1))
                {
                    Fire_Net(last_dir);
                    last_dir = -1; // 방향 초기화
                }
				game_over = Frog_Move(Jog_key);//무조건 0 리턴
				Jog_key_in = 0;
			}

            if(TIM4_expired)
            {
                TIM4_expired = 0;
            }

			if(SysTick_Flag) //100ms
			{
                SysTick_Flag = 0;
                if(frog.stop > 0) // 100ms마다 카운트 감소
                {
                    frog.stop--; 
                }
                if(fly_CNT == 6)
                {
                    level = 1;
                }
                Update_Projectile(); // 발사체 위치 업데이트
                if(human_stop_counter > 0) 
                {
                    human_stop_counter--;
                    if(human_stop_counter == 0) {
                        human_stopped = 0;
                    }
                }
                int i;
                for(i=0; i<2; i++) 
                {
                    if(snake_stop_counter[i] > 0) 
                    {
                        snake_stop_counter[i]--;
                        if(snake_stop_counter[i] == 0) 
                        {
                            snake_stopped[i] = 0;
                        }
                    }
                }
                if(fly.dir == -1)// fly가 포획된 경우
                {
                    if(fly_CNT <= 7)
                    { 
                        if(fly_reset_tim < 50)
                        {
                            if(fly_reset_tim == 0)
                            {
                                if(fly_CNT <= 6)
                                {
                                    Uart_Printf("come here\nfly death %d\n\n", fly_CNT); 
                                }
                                else//fly_CNT==7
                                {
                                    Uart_Printf("fly death %d\n\n", fly_CNT); 
                                    Uart_Printf("bring me that food...........\n                              -frog_son-\n"); 
                                }
                            }   
                            fly_reset_tim++;
                        }     
                    }
                    if((fly_reset_tim == 50) && (game_over == 0) && (game_clear ==0))// fly가 개구리에게 포획된 후, 5초 뒤 다른 위치에서 탄생
                    {
                        Fly_Move();
                        fly.dir = 0;
                        fly_reset_tim = 0;
                    }
                    if(fly_CNT == 8)// GAME CLEAR !!!
                    {
                        game_clear = 1;
                    }
                }
                if((fly_CNT == 5)||(level == 1)) // human 활성화
                { 
                    human.dir = 0;
                    Lcd_Draw_Box(human.x, human.y, human.w, human.h, human.ci);
                    game_over += Check_Collision(&frog, &human);
                }
                if(human.dir == 0) // human 이동 로직 추가
                {
                    game_over += Human_Move();
                }
                game_over += Snake_Move() + Check_Collision(&frog, &snake[0]) + Check_Collision(&frog, &snake[1]) + Check_Collision(&frog, &fly);
                game_over += Check_Collision(&frog, &poison[0]) + Check_Collision(&frog, &poison[1]) + Check_Collision(&frog, &poison[2]) + Check_Collision(&frog, &poison[3]);
                if(level == 1) // HARD MODE || easy mode fly 5이상
                {
                    game_over += Check_Collision(&frog, &human);
                }
            }
            if(game_over)
            {
				TIM3_Out_Stop();
				song_on = 0;//노래off -> 노래 처음으로 복귀
                GAMEOVER_func();
                break;
            }
            if(game_clear)
            {
				TIM3_Out_Stop();
				song_on = 0;
                GAMECLEAR_func();
                break;
            }
		}
        song_on = 0;
	}
}

void LCD_INITIAL_Display(void)
{
	Lcd_Draw_Back_Color(WHITE);//흰화면
    Lcd_Draw_Box(40, 0, 40, Y_MAX, BLUE);
    Lcd_Draw_Box(80, 0, 40, Y_MAX, RED);
    Lcd_Draw_Box(120, 0, 40, Y_MAX, YELLOW);
    Lcd_Draw_Box(160, 0, 40, Y_MAX, BLACK);
    Lcd_Draw_Box(200, 0, 40, Y_MAX, WHITE);
    Lcd_Draw_Box(240, 0, 40, Y_MAX, NAVY);
    Lcd_Draw_Box(280, 0, 40, Y_MAX, GREEN);

	while(!Jog_key_in);// 조이스틱 건들면 다음 페이지
    Jog_key_in=0;

    Lcd_Clr_Screen();
    Lcd_Printf(20, 100, DARKGREEN, WHITE, 2, 2, "Makjang FROGGGGGY");
    TIM2_Delay(500);
    while(!Jog_key_in);// 조이스틱 건들면 다음 페이지
    Jog_key_in=0;

    Lcd_Clr_Screen();
    Lcd_Printf(60, 100, RED, WHITE, 2, 2, "EASY<==>HARD");
    TIM2_Delay(500);
    while(!Jog_key_in);// 조이스틱 건들면 다음 페이지
    Jog_key_in=0;

    Lcd_Clr_Screen();
    if(Jog_key==5) { Lcd_Printf(10, 100, BLACK, WHITE, 1, 1, "YOUR CHOICE: HARD MODE"); level = 1; }
    else { Lcd_Printf(10, 100, BLACK, WHITE, 1, 1, "YOUR CHOICE: EASY MODE"); level = 0; }
    TIM2_Delay(500);
    while(!Jog_key_in);// 조이스틱 건들면 다음 페이지
    Jog_key_in=0;
        
    Lcd_Clr_Screen();
}

static int Check_Wall_Collision(int new_x, int new_y, int w, int h)
{
    int col_start = new_x / MAZE_CELL_SIZE;
    int row_start = new_y / MAZE_CELL_SIZE;
    int col_end = (new_x + w) / MAZE_CELL_SIZE;
    int row_end = (new_y + h) / MAZE_CELL_SIZE;
	int i, j;

    for(i=row_start; i<=row_end; i++) 
	{
        for(j=col_start; j<=col_end; j++) 
		{
            if(maze[i][j] == 1) return 1; // 충돌
        }
    }
    return 0; // 충돌 없음
}

static int Check_Collision(FROGs * obj1, QUERY_DRAW * obj2)
{// obj1:개구리, obj2:충돌대상
    if(obj2->dir != -1)
    {
        if((obj1->x>obj2->x+obj2->w)||(obj1->x+obj1->w<obj2->x)||(obj1->y+obj1->h<obj2->y)||(obj1->y>obj2->y+obj2->h)) { }// 충돌 x
        else // 충돌 
        {
            if((obj2 == &snake[0]) || (obj2 == &snake[1]) || (obj2 == &human))
            {//GAMEOVER
                return 1;
            }
            else
            {
                if(obj2 == &poison[0]) { frog.stop = 30; eat_poison++; poison[0].dir = -1;}
                else if(obj2 == &poison[1]) { frog.stop = 30; eat_poison++; poison[1].dir = -1;}
                else if(obj2 == &poison[2]) { frog.stop = 30; eat_poison++; poison[2].dir = -1;}
                else if(obj2 == &poison[3]) { frog.stop = 30; eat_poison++; poison[3].dir = -1;}
                else { fly_CNT++; }//파리와 부딪히는 경우
                obj2->dir=-1;
                Lcd_Draw_Box(obj2->x, obj2->y, obj2->w, obj2->h, BACK_COLOR);
                Lcd_Draw_Box(frog.x, frog.y, frog.w, frog.h, frog.ci);
            }
        }
    }
    else//obj2가 이미 죽은 경우
    {
        return 0;
    }
    return 0;
}

static void k0(void)
{
	if(frog.y > Y_MIN) frog.y -= FROG_STEP;
}

static void k1(void)
{
	if(frog.y + frog.h < Y_MAX) frog.y += FROG_STEP;
}

static void k2(void)
{
	if(frog.x > X_MIN) frog.x -= FROG_STEP;
}

static void k3(void)
{
	if(frog.x + frog.w < X_MAX) frog.x += FROG_STEP;
}

void Init_Projectile(void) 
{
    projectile.active = 0;
    projectile.speed = 10; // 이동 속도
    projectile.distance = 0; // 거리 초기화 
}

void Fire_Net(int dir) 
{
    if(!projectile.active) 
    {   
        // 개구리 중심 좌표 계산
        projectile.x = frog.x + frog.w/2;
        projectile.y = frog.y + frog.h/2;
        switch(dir) 
        {
            case 0: projectile.y -= projectile.speed; break; // 상
            case 1: projectile.y += projectile.speed; break; // 하
            case 2: projectile.x -= projectile.speed; break; // 좌
            case 3: projectile.x += projectile.speed; break; // 우
        }
        projectile.dir = dir;
        projectile.active = 1;
        projectile.distance = 0; // 발사 시 거리 초기화 
    }
}

void Update_Projectile(void)
{
    if(projectile.active) {
        // 이전 위치 지우기
        Lcd_Draw_Box(projectile.x-2, projectile.y-2, 5, 5, BLACK);
        int i, j;
        for(i=0; i<MAZE_ROWS; i++) 
        {
            for(j=0; j<MAZE_COLS; j++) 
            {
                if(maze[i][j] == 1) 
                {
                    Lcd_Draw_Box(j*MAZE_CELL_SIZE, i*MAZE_CELL_SIZE, MAZE_CELL_SIZE, MAZE_CELL_SIZE, RED);
                }
            }
        }
        Lcd_Draw_Box((15*MAZE_CELL_SIZE - 25), (11*MAZE_CELL_SIZE + 5), 70, 10, BLACK);
        // 방향에 따른 이동
        switch(projectile.dir) 
        {
            case 0: projectile.y -= projectile.speed; break; // 상
            case 1: projectile.y += projectile.speed; break; // 하
            case 2: projectile.x -= projectile.speed; break; // 좌
            case 3: projectile.x += projectile.speed; break; // 우
        }
        
        projectile.distance += projectile.speed; // 거리 업데이트
        
        // 사정거리(32) 초과 시 제거
        if(projectile.distance >= 32) 
        { 
            projectile.active = 0;
            return;
        }

        if((projectile.x-2 < human.x + human.w) && (projectile.x+2 > human.x) && (projectile.y-2 < human.y + human.h) && (projectile.y+2 > human.y))
        {
            human_stopped = 1;
            human_stop_counter = 20;
            projectile.active = 0;
            return;
        }

        // 벽 충돌 검사
        int col = projectile.x / MAZE_CELL_SIZE;
        int row = projectile.y / MAZE_CELL_SIZE;
        if(maze[row][col] == 1) 
        {
            projectile.active = 0;
            return;
        }

        for(i=0; i<2; i++) 
        {
            if((projectile.x-2 < snake[i].x + snake[i].w) && (projectile.x+2 > snake[i].x) && (projectile.y-2 < snake[i].y + snake[i].h) && (projectile.y+2 > snake[i].y)) 
            {
                snake_stopped[i] = 1;
                snake_stop_counter[i] = 20;
                projectile.active = 0;
                return;
            }
        }
        
        // 화면 경계 검사
        if((projectile.x < 0) || (projectile.x > LCDW) || (projectile.y < 0) || (projectile.y > LCDH)) 
        {
            projectile.active = 0;
            return;
        }
        
        Lcd_Draw_Box(projectile.x-2, projectile.y-2, 5, 5, WHITE);// 새 위치 그리기 (흰색 네모)
    }
}

static int Frog_Move(int k) 
{
    if(frog.stop == 0)
    {
        int prev_x = frog.x;
        int prev_y = frog.y;
    
        static void (*key_func[])(void) = {k0, k1, k2, k3};
        
        frog.ci = BACK_COLOR;
        Lcd_Draw_Box(frog.x, frog.y, frog.w, frog.h, frog.ci);
    
        if(k <= 3) key_func[k]();
    
        if(Check_Wall_Collision(frog.x, frog.y, frog.w, frog.h)) 
        {
            frog.x = prev_x; // 충돌 시 위치 복원
            frog.y = prev_y;
        }
    }

    frog.ci = FROG_COLOR;
    Lcd_Draw_Box(frog.x, frog.y, frog.w, frog.h, frog.ci);
    
    return 0;
}

static int Snake_Move(void)
{
    int step;
    if(level == 0)
    {
        step = FROG_STEP;
    }
    else
    {
        step = FROG_STEP + 1;
    }
    // 뱀1
    if(!snake_stopped[0]) 
    {
        snake[0].ci = BACK_COLOR;
        Lcd_Draw_Box(snake[0].x, snake[0].y, snake[0].w, snake[0].h, snake[0].ci);
        if(snake[0].dir == 0) // 우
        {
            snake[0].x += step;  
        }   
        else // 좌
        {
            snake[0].x -= step;  
        }
        if((snake[0].x >= 10 * MAZE_CELL_SIZE)||(snake[0].x < 5 * MAZE_CELL_SIZE))
        {
            if(snake[0].dir == 0) 
            {
                snake[0].dir = 1;// 좌
                snake[0].x -= 2 * step;  
            }
            else 
            {
                snake[0].dir = 0;// 우
                snake[0].x += 2 * step; 
            }
        }
        snake[0].ci = SNAKE_COLOR;
        Lcd_Draw_Box(snake[0].x, snake[0].y, snake[0].w, snake[0].h, snake[0].ci);
    }

    // 뱀2
    if(!snake_stopped[1]) 
    {
        snake[1].ci = BACK_COLOR;
        Lcd_Draw_Box(snake[1].x, snake[1].y, snake[1].w, snake[1].h, snake[1].ci);

        if(snake[1].dir == 3) // 아래
        {
            snake[1].y += step;    
        }
        else // 위
        {
            snake[1].y -= step; 
        }
        if((snake[1].y > 10 * MAZE_CELL_SIZE) || (snake[1].y < 7 * MAZE_CELL_SIZE))
        {
            if(snake[1].dir == 3) 
            {
                snake[1].dir = 2;// 아래
                snake[1].y -= 2 * step; 
            }
            else 
            {
                snake[1].dir = 3;// 위
                snake[1].y += 2 * step; 
            }
        }
        snake[1].ci = SNAKE_COLOR;
        Lcd_Draw_Box(snake[1].x, snake[1].y, snake[1].w, snake[1].h, snake[1].ci);
    }

    return 0;
}

static int simple_rand(int min, int max) 
{
    rand_seed ^= TIM4->CNT;
    rand_seed = (rand_seed * 214013UL + 2531011UL);
    rand_seed ^= (TIM4->CNT << 8); // 추가 혼합

    int range = max - min + 1;
    int r = (rand_seed % range);
    if(r < 0) r = -r; // 음수 방지

    return min + r;
}

// fly 위치 유효성 검사 (1: 유효, 0: 무효)
static int Is_Valid_Fly_Position(int fly_col, int fly_row) 
{
    // frog와의 거리 계산 (최소 4칸 이상)
    int frog_col = (frog.x + frog.w/2) / MAZE_CELL_SIZE;
    int frog_row = (frog.y + frog.h/2) / MAZE_CELL_SIZE;
    int x, y;

    if(fly_col - frog_col < 0)
    {
        x = -(fly_col - frog_col);
    }
    else
    {
        x = (fly_col - frog_col);
    }
    if(fly_row - frog_row < 0)
    {
        y = -(fly_row - frog_row);
    }
    else
    {
        y = (fly_row - frog_row);
    }

    int dist = x + y;
    if(dist < 4) { return 0; }

    // snake[0]의 이동 영역 회피 (col 5~10)
    if(fly_col >= 5 && fly_col <= 10) { return 0; }
    
    // snake[1]의 이동 영역 회피 (row 7~10)
    if(fly_row >= 7 && fly_row <= 10) { return 0; }
    
    // 벽이 아닌지 확인
    return (maze[fly_row][fly_col] == 0);
}

static void Fly_Move(void)
{
    if((fly_CNT >= 4) && (fly_CNT <= 5)) 
    {
        rand_seed = TIM4_expired; // TIM4 카운터로 시드 초기화
        
        int attempts = 0;
        int valid = 0;
        int fly_col, fly_row;
        
        // 최대 50회 시도
        while((!valid) && (attempts++ < 50)) 
        {
            fly_col = simple_rand(1, MAZE_COLS-2); // 1~14
            fly_row = simple_rand(1, MAZE_ROWS-2); // 1~10
            valid = Is_Valid_Fly_Position(fly_col, fly_row);
        }
        
        if(valid) 
        {
            fly.x = fly_col * MAZE_CELL_SIZE + 8;
            fly.y = fly_row * MAZE_CELL_SIZE + 8;
        } 
        else 
        { // 유효한 위치 못 찾을 경우 기본 위치
            fly.x = 8 * MAZE_CELL_SIZE + 8;
            fly.y = 5 * MAZE_CELL_SIZE + 8;
        }
    } 
    else if(fly_CNT == 6)//fly 7마리 마지막 생성시기
    {
        if(frog.x<160)
        {
            fly.x = 0 * MAZE_CELL_SIZE + 8;
            fly.y = 5 * MAZE_CELL_SIZE + 8;
            dest_x = 15 * MAZE_CELL_SIZE + 8;
            dest_y = fly.y = 5 * MAZE_CELL_SIZE + 8;
        }
        else
        {
            fly.x = 15 * MAZE_CELL_SIZE + 8;
            fly.y = 5 * MAZE_CELL_SIZE + 8;
            dest_x = 0 * MAZE_CELL_SIZE + 8;
            dest_y = fly.y = 5 * MAZE_CELL_SIZE + 8;
        }
		maze[5][0] = 0;
		maze[5][15] = 0;
		Lcd_Draw_Box(0*MAZE_CELL_SIZE, 5*MAZE_CELL_SIZE, MAZE_CELL_SIZE, MAZE_CELL_SIZE, BLACK);
        Lcd_Draw_Box(15*MAZE_CELL_SIZE, 5*MAZE_CELL_SIZE, MAZE_CELL_SIZE, MAZE_CELL_SIZE, BLACK);
        level = 1;
        fly.ci = DARKGREEN;//개구리밥 표현
    }
    else if(fly_CNT == 7)
    {
        fly.x = dest_x;
        fly.y = dest_y;
    }
    else if(fly_CNT < 4)
    {
        if(frog.x>=160)
        {
            if(frog.y>=120)
            {
                fly.x = 1 * MAZE_CELL_SIZE + 8;
                fly.y = 1 * MAZE_CELL_SIZE + 8;
            }
            else
            {
                fly.x = 1 * MAZE_CELL_SIZE + 8;
                fly.y = 10 * MAZE_CELL_SIZE + 8;
            }
        }
        else
        {
            if(frog.y>=120)
            {
                fly.x = 14 * MAZE_CELL_SIZE + 8;
                fly.y = 1 * MAZE_CELL_SIZE + 8;
            }
            else
            {
                fly.x = 14 * MAZE_CELL_SIZE + 8;
                fly.y = 9 * MAZE_CELL_SIZE + 8;
            }
        }
    }
    Lcd_Draw_Box(fly.x, fly.y, fly.w, fly.h, fly.ci);
}

// poison_index: poison[0]~poison[3] 중 어디에 둘지 인덱스
static void Place_Poison(int poison_index) 
{
    int attempts = 0;
    int max_attempts = 100;
    int col, row;
    int valid = 0;
    int i;
    rand_seed = TIM4_expired + poison_index * 17; // 시드 갱신

    while((!valid) && (attempts++ < max_attempts)) 
    {
        col = simple_rand(1, MAZE_COLS-2); // 1~14
        row = simple_rand(1, MAZE_ROWS-2); // 1~10
        // 1. 벽이 아니고
        if(maze[row][col] != 0) continue;

        // 2. snake[0], snake[1]의 현재 위치와 겹치지 않음
        int snake0_col = (snake[0].x + snake[0].w/2) / MAZE_CELL_SIZE;
        int snake0_row = (snake[0].y + snake[0].h/2) / MAZE_CELL_SIZE;
        int snake1_col = (snake[1].x + snake[1].w/2) / MAZE_CELL_SIZE;
        int snake1_row = (snake[1].y + snake[1].h/2) / MAZE_CELL_SIZE;
        if((col == snake0_col && row == snake0_row) || (col == snake1_col && row == snake1_row)) continue;

        // 3. 이미 다른 poison과 겹치지 않음
        int overlap = 0;
        for(i=0; i<4; i++) 
        {
            if(i == poison_index) { continue; }

            int p_col = (poison[i].x + poison[i].w/2) / MAZE_CELL_SIZE;
            int p_row = (poison[i].y + poison[i].h/2) / MAZE_CELL_SIZE;

            if(col == p_col && row == p_row && poison[i].dir != -1) 
            {
                overlap = 1;
                break;
            }
        }
        if(overlap) { continue; }
        valid = 1;
    }

    if(valid) 
    {
        poison[poison_index].x = col * MAZE_CELL_SIZE + 8;
        poison[poison_index].y = row * MAZE_CELL_SIZE + 8;
        poison[poison_index].w = FROG_SIZE_X - 5;
        poison[poison_index].h = FROG_SIZE_X - 5;
        poison[poison_index].ci = GRAY;
        poison[poison_index].dir = 0; // 활성화x
        Lcd_Draw_Box(poison[poison_index].x, poison[poison_index].y, poison[poison_index].w, poison[poison_index].h, poison[poison_index].ci);
    }
}

static int Human_Move(void) 
{
    if(human.dir != 0 || human_stopped) return 0;
    
    int dx_fly = (fly.x > frog.x) ? (fly.x - frog.x) : (frog.x - fly.x);
    int dy_fly = (fly.y > frog.y) ? (fly.y - frog.y) : (frog.y - fly.y);
    
    // fly 주변 100px 이내에 frog가 있으면 추적 시작
    if(dx_fly < 100 && dy_fly < 100) 
    {
        int prev_x = human.x;
        int prev_y = human.y;
        int step = 1;

        // 이전 위치 지우기
        Lcd_Draw_Box(human.x, human.y, human.w, human.h, BACK_COLOR);

        // X축 이동
        if(human.x < frog.x) { human.x += step; }
        else if(human.x > frog.x) { human.x -= step; }

        // X축 충돌 검사
        if(Check_Wall_Collision(human.x, human.y, human.w, human.h)) 
        {
            human.x = prev_x; // 충돌 시 X축 복원
        }

        // Y축 이동
        if(human.y < frog.y) { human.y += step; }
        else if(human.y > frog.y) { human.y -= step; }

        // Y축 충돌 검사
        if(Check_Wall_Collision(human.x, human.y, human.w, human.h)) 
        {
            human.y = prev_y; // 충돌 시 Y축 복원
        }
        // 새 위치 그리기
        Lcd_Draw_Box(human.x, human.y, human.w, human.h, human.ci);
    }
    return 0;
}

void Game_Init(void) 
{
	start = 1;
    song_on = 1;
    fly_CNT = 5;
    eat_poison = 0;
    
	int i, j;
	
	Lcd_Clr_Screen();
    Init_Projectile(); // 발사체 초기화

    // 미로 그리기
    for(i=0; i<MAZE_ROWS; i++) 
	{
        for(j=0; j<MAZE_COLS; j++) 
		{
            if(maze[i][j] == 1) 
			{
                Lcd_Draw_Box(j*MAZE_CELL_SIZE, i*MAZE_CELL_SIZE, MAZE_CELL_SIZE, MAZE_CELL_SIZE, RED);
            }
        }
    }
    //시작 가능한 위치 수집
	empty_cell_count = 0;

	for(i=0; i<MAZE_ROWS; i++) 
	{
		for(j=0; j<MAZE_COLS; j++) 
		{
			if((maze[i][j] == 0) && (empty_cell_count < MAX_EMPTY_CELLS)) 
			{
				empty_cells[empty_cell_count][0] = i;
				empty_cells[empty_cell_count][1] = j;
				empty_cell_count++;
			}
		}
	}
	// 개구리 초기 상태 설정 (첫 번째 비벽 셀)
	if (empty_cell_count > 0) 
	{
		frog.x = empty_cells[0][1] * MAZE_CELL_SIZE + 5;
		frog.y = empty_cells[0][0] * MAZE_CELL_SIZE + 5;
	}
	else // 예외 처리: 가능한 위치가 없을 경우
	{
		frog.x = 150;  // 기본 위치
		frog.y = 220;
	}
    frog.w = FROG_SIZE_X; 
	frog.h = FROG_SIZE_Y;
	frog.ci = FROG_COLOR;
	frog.dir = 0;
    frog.stop = 0;
	Lcd_Draw_Box(frog.x, frog.y, frog.w, frog.h, frog.ci);

    // 뱀1 초기 위치 설정
    snake[0].x = 6 * MAZE_CELL_SIZE + 3;
    snake[0].y = 2 * MAZE_CELL_SIZE + 3;
    snake[0].w = FROG_SIZE_X + 4; 
	snake[0].h = FROG_SIZE_Y + 4;
    snake[0].ci = SNAKE_COLOR;
    snake[0].dir = 0;// 0: 우, 1: 좌
    Lcd_Draw_Box(snake[0].x, snake[0].y, snake[0].w, snake[0].h, snake[0].ci);

    // 뱀2 초기 위치 설정
    snake[1].x = 7 * MAZE_CELL_SIZE + 3;
    snake[1].y = 7 * MAZE_CELL_SIZE + 3;
    snake[1].w = FROG_SIZE_X + 4; 
	snake[1].h = FROG_SIZE_Y + 4;
    snake[1].ci = SNAKE_COLOR;
    snake[1].dir = 3;// 2: 위, 3: 아래
    Lcd_Draw_Box(snake[1].x, snake[1].y, snake[1].w, snake[1].h, snake[1].ci);

    // 모기 초기 위치 설정
    fly.x = 7 * MAZE_CELL_SIZE + 8;
    fly.y = 5 * MAZE_CELL_SIZE + 8;
    fly.w = FROG_SIZE_X - 5; 
	fly.h = FROG_SIZE_Y - 5;
    fly.ci = FLY_COLOR;
    fly.dir = 3;// 2: 위, 3: 아래
    Lcd_Draw_Box(fly.x, fly.y, fly.w, fly.h, fly.ci);

    for(i=0;i<4;i++)
    {
        Place_Poison(i);
    }

    // 인간 초기 상태 설정
    human.x = 1 * MAZE_CELL_SIZE + 2;
    human.y = 5 * MAZE_CELL_SIZE + 2;
    human.w = FROG_SIZE_X + 5;
    human.h = FROG_SIZE_X + 5;
    human.ci = ORANGE;
    human.dir = -1;
}

void LCD_GAMEOVER_Display(void)//gameover LCD화면
{
    Lcd_Clr_Screen();
    draw_image(150, 30, &frog_gameover);
    Lcd_Printf(60, 100, RED, WHITE, 2, 2, "GAMEOVER");
    Lcd_Printf(60, 130, RED, WHITE, 2, 2, "zzzzzzzzzzz ^_^");
    while(!Jog_key_in);// 조이스틱 건들면 다음 페이지
    Jog_key_in=0;
}

void LCD_GAMECLEAR_Display(void)//gameclear LCD화면
{
    Lcd_Clr_Screen();
    draw_image(0, 0, &frog_gameclear);
    Lcd_Printf(60, 100, GREEN, WHITE, 2, 2, "GAMECLEAR");
    Lcd_Printf(30, 130, GREEN, WHITE, 2, 2, "^_^ UNBELIEVABLE!!");

    while(!Jog_key_in);// 조이스틱 건들면 다음 페이지
    Jog_key_in=0;

    Lcd_Draw_Back_Color(PINK);
    Lcd_Printf(30, 130, BLACK, PINK, 2, 2, "^_^ I'm HAPPY");
    while(!Jog_key_in);// 조이스틱 건들면 다음 페이지
    Jog_key_in=0;
}

void GAMEOVER_func(void)
{
    Uart_Printf("Game Over, Please press any key to continue.\n");
    Lcd_Printf(0, 100, BLACK, WHITE, 1, 1, "press any key to continue");
    Jog_Wait_Key_Pressed();
    TIM2_Delay(500);
    Jog_Wait_Key_Released();
    TIM2_Delay(500);
    LCD_GAMEOVER_Display();
    Uart_Printf("Game Start\n");
}

void GAMECLEAR_func(void)
{
    LCD_GAMECLEAR_Display();
    Lcd_Clr_Screen();
}