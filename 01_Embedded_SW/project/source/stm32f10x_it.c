/**
  ******************************************************************************
  * @file    Project/STM32F10x_StdPeriph_Template/stm32f10x_it.c 
  * @author  MCD Application Team
  * @version V3.5.0
  * @date    08-April-2011
  * @brief   Main Interrupt Service Routines.
  *          This file provides template for all exceptions handler and 
  *          peripherals interrupt service routine.
  ******************************************************************************
  * @attention
  *
  * THE PRESENT FIRMWARE WHICH IS FOR GUIDANCE ONLY AIMS AT PROVIDING CUSTOMERS
  * WITH CODING INFORMATION REGARDING THEIR PRODUCTS IN ORDER FOR THEM TO SAVE
  * TIME. AS A RESULT, STMICROELECTRONICS SHALL NOT BE HELD LIABLE FOR ANY
  * DIRECT, INDIRECT OR CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING
  * FROM THE CONTENT OF SUCH FIRMWARE AND/OR THE USE MADE BY CUSTOMERS OF THE
  * CODING INFORMATION CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.
  *
  * <h2><center>&copy; COPYRIGHT 2011 STMicroelectronics</center></h2>
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/

#include "device_driver.h"

void Invalid_ISR(void)
{
  Uart1_Printf("Invalid_Exception: %d!\n", Macro_Extract_Area(SCB->ICSR, 0x1ff, 0));
  Uart1_Printf("Invalid_ISR: %d!\n", Macro_Extract_Area(SCB->ICSR, 0x1ff, 0) - 16);
  for(;;);
}

static char * const Stack_reg[] = {"R0","R1","R2","R3","R12","LR","RA","xPSR"};

static void Stack_Dump(const char * stack, unsigned int * sp)
{
	int i;

	for(i=0; i<(sizeof(Stack_reg)/sizeof(Stack_reg[0])); i++)
	{
		Uart1_Printf("%s[%d],%s=0x%.8X\n", stack, i, Stack_reg[i], sp[i]);
	}
}

static void Fault_Report(unsigned int * msp, unsigned int lr, unsigned int * psp)
{
	Uart1_Printf("LR(EXC_RETURN)=0x%.8X\n", lr);
	Uart1_Printf("MSP=0x%.8X\n", msp);
	Uart1_Printf("PSP=0x%.8X\n", psp);

	switch((lr & (0xF<<28))|(lr & 0xF))
	{
		case 0xF0000001: Uart1_Printf("Exception occurs from handler mode\n"); Stack_Dump("MSP", msp); break;
		case 0xF0000009: Uart1_Printf("Exception occurs from thread mode with MSP\n"); Stack_Dump("MSP", msp); break;
		case 0xF000000d: Uart1_Printf("Exception occurs from thread mode with PSP\n"); Stack_Dump("PSP", psp); break;
		default: Uart1_Printf("Invalid exception return value => %#.8X\n", lr & 0xf); break;
	}

	Uart1_Printf("SHCSR => %#.8X\n", SCB->SHCSR);
	Uart1_Printf("CFSR(Fault Reason) => %#.8X\n", SCB->CFSR);
}

/*******************************************************************************
 * Function Name  : NMIException
 * Description    : This function handles NMI exception.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void NMI_Handler(void)
{
	Uart1_Printf("NMI!\n");
	for(;;);
}

/*******************************************************************************
 * Function Name  : HardFaultException
 * Description    : This function handles Hard Fault exception.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void HardFault_Handler(unsigned int * msp, unsigned int lr, unsigned int * psp)
{
	Uart1_Printf("Hard Fault!\n");

	Fault_Report(msp, lr, psp);

	Uart1_Printf("MMFAR Valid => %d\n", Macro_Check_Bit_Set(SCB->CFSR, 7));
	Uart1_Printf("MMFAR => %#.8X\n", SCB->MMFAR);
	Uart1_Printf("BFAR Valid => %d\n", Macro_Check_Bit_Set(SCB->CFSR, 15));
	Uart1_Printf("BFAR => %#.8X\n", SCB->BFAR);
	Uart1_Printf("HFSR(Hard Fault Reason) => %#.8X\n", SCB->HFSR);

	for(;;);
}

/*******************************************************************************
 * Function Name  : MemManageException
 * Description    : This function handles Memory Manage exception.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void MemManage_Handler(unsigned int * msp, unsigned int lr, unsigned int * psp)
{
	Uart1_Printf("Memory Management Fault!\n");
	for(;;);
}

/*******************************************************************************
 * Function Name  : BusFaultException
 * Description    : This function handles Bus Fault exception.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void BusFault_Handler(unsigned int * msp, unsigned int lr, unsigned int * psp)
{
	Uart1_Printf("Bus Fault!\n");
	for(;;);
}

/*******************************************************************************
 * Function Name  : UsageFaultException
 * Description    : This function handles Usage Fault exception.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void UsageFault_Handler(unsigned int * msp, unsigned int lr, unsigned int * psp)
{
	Uart1_Printf("Usage Fault!\n");
	for(;;);
}

/*******************************************************************************
 * Function Name  : SVCHandler
 * Description    : This function handles SVCall exception.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void SVC_Handler(void)
{
	Uart1_Printf("SVC Call\n");
	for(;;);
}

/*******************************************************************************
 * Function Name  : DebugMonitor
 * Description    : This function handles Debug Monitor exception.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void DebugMon_Handler(void)
{
	Uart1_Printf("DebugMon Call\n");
	for(;;);
}

/*******************************************************************************
 * Function Name  : PendSVC
 * Description    : This function handles PendSVC exception.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void PendSV_Handler(void)
{
	Uart1_Printf("PendSV Call\n");
	for(;;);
}

/*******************************************************************************
 * Function Name  : SysTickHandler
 * Description    : This function handles SysTick Handler.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
volatile int SysTick_Flag = 0;

void SysTick_Handler(void)
{
	SysTick_Flag = 1;
}

/*******************************************************************************
 * Function Name  : WWDG_IRQHandler
 * Description    : This function handles WWDG interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void WWDG_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : PVD_IRQHandler
 * Description    : This function handles PVD interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void PVD_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : TAMPER_IRQHandler
 * Description    : This function handles Tamper interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void TAMPER_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : RTC_IRQHandler
 * Description    : This function handles RTC global interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void RTC_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : FLASH_IRQHandler
 * Description    : This function handles Flash interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void FLASH_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : RCC_IRQHandler
 * Description    : This function handles RCC interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void RCC_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : EXTI0_IRQHandler
 * Description    : This function handles External interrupt Line 0 request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void EXTI0_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : EXTI1_IRQHandler
 * Description    : This function handles External interrupt Line 1 request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void EXTI1_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : EXTI2_IRQHandler
 * Description    : This function handles External interrupt Line 2 request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void EXTI2_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : EXTI3_IRQHandler
 * Description    : This function handles External interrupt Line 3 request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
 volatile int Jog_key_in = 0;
 volatile int Jog_key = 0;
 
 void EXTI3_IRQHandler(void)
 {
   // UP
   Jog_key_in = 1;
   Jog_key = 0;
   EXTI->PR = 0x1<<3;
   NVIC_ClearPendingIRQ(EXTI3_IRQn);
 }

/*******************************************************************************
 * Function Name  : EXTI4_IRQHandler
 * Description    : This function handles External interrupt Line 4 request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void EXTI4_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : DMA1_Channel1_IRQHandler
 * Description    : This function handles DMA1 Channel 1 interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void DMA1_Channel1_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : DMA1_Channel2_IRQHandler
 * Description    : This function handles DMA1 Channel 2 interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void DMA1_Channel2_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : DMA1_Channel3_IRQHandler
 * Description    : This function handles DMA1 Channel 3 interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void DMA1_Channel3_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : DMA1_Channel4_IRQHandler
 * Description    : This function handles DMA1 Channel 4 interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void DMA1_Channel4_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : DMA1_Channel5_IRQHandler
 * Description    : This function handles DMA1 Channel 5 interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void DMA1_Channel5_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : DMA1_Channel6_IRQHandler
 * Description    : This function handles DMA1 Channel 6 interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void DMA1_Channel6_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : DMA1_Channel7_IRQHandler
 * Description    : This function handles DMA1 Channel 7 interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void DMA1_Channel7_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : ADC1_2_IRQHandler
 * Description    : This function handles ADC1 and ADC2 global interrupts requests.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void ADC1_2_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : USB_HP_CAN_TX_IRQHandler
 * Description    : This function handles USB High Priority or CAN TX interrupts
 *                  requests.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void USB_HP_CAN_TX_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : USB_LP_CAN_RX0_IRQHandler
 * Description    : This function handles USB Low Priority or CAN RX0 interrupts
 *                  requests.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void USB_LP_CAN_RX0_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : CAN_RX1_IRQHandler
 * Description    : This function handles CAN RX1 interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void CAN_RX1_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : CAN_SCE_IRQHandler
 * Description    : This function handles CAN SCE interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void CAN_SCE_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : EXTI9_5_IRQHandler
 * Description    : This function handles External lines 9 to 5 interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
 void EXTI9_5_IRQHandler(void)
 {
   // RLD
   static int EXTI9_5_LUT[8] = {0,1,2,0,3,0,0,0};
   Jog_key = EXTI9_5_LUT[Macro_Extract_Area(EXTI->PR,0x7,5)];
   Jog_key_in = 1;
   EXTI->PR = 0x7<<5;
   NVIC_ClearPendingIRQ(EXTI9_5_IRQn);
 }

/*******************************************************************************
 * Function Name  : TIM1_BRK_IRQHandler
 * Description    : This function handles TIM1 Break interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void TIM1_BRK_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : TIM1_UP_IRQHandler
 * Description    : This function handles TIM1 overflow and update interrupt
 *                  request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void TIM1_UP_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : TIM1_TRG_COM_IRQHandler
 * Description    : This function handles TIM1 Trigger and commutation interrupts
 *                  requests.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void TIM1_TRG_COM_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : TIM1_CC_IRQHandler
 * Description    : This function handles TIM1 capture compare interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void TIM1_CC_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : TIM2_IRQHandler
 * Description    : This function handles TIM2 global interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void TIM2_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : TIM3_IRQHandler
 * Description    : This function handles TIM3 global interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void TIM3_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : TIM4_IRQHandler
 * Description    : This function handles TIM4 global interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
 volatile int TIM4_expired = 0;
 volatile int song_on = 1;
 volatile int start = 1;
 volatile int n = 0;
 volatile int i = 0;

 static void Buzzer_Beep(unsigned char tone, int duration) 
{
  const static unsigned short tone_value[] = {
      261,277,293,311,329,349,369,391,415,440,466,493,
      523,554,587,622,659,698,739,783,830,880,932,987
  };
  TIM3_Out_Freq_Generation(tone_value[tone]);
}

 void TIM4_IRQHandler(void)
 {
   // 음계 인덱스 (기존 enum key 확장)
   enum key {
    C1, C1_, D1, D1_, E1, F1, F1_, G1, G1_, A1, B1,
    C2, C2_, D2, E2, F2, F2_, G2, G2_, A2, A2_, B2,
    GS1 = 8,   // G#1 (415Hz)
    GS2 = 20,  // G#2 (830Hz)
    A1_ = 9,   // A#1 (466Hz)
    D2_ = 15    // D#2 (622Hz)
  };

  // 이집트풍 노래 데이터 (게임 시작 시 재생)
  const int egyptian_start_song[][2] = {
    // Intro: 기존 멜로디 반복
    {E1, 200}, {F1, 100}, {GS1, 200}, {A1, 400}, 
    {GS1, 100}, {F1, 100}, {E1, 300}, {0, 100},
    {E1, 200}, {F1, 100}, {GS1, 200}, {A1, 400},
    {GS1, 100}, {F1, 100}, {E1, 300}, {0, 100},
  
    // Verse: 상승/하강 패턴 추가
    {B1, 150}, {A1_, 150}, {GS1, 300}, {F1, 150},
    {E1, 150}, {F1, 150}, {GS1, 300}, {A1, 450},
    {GS1, 150}, {F1, 150}, {E1, 300}, {D1_, 150},
    {C2, 150}, {B1, 300}, {0, 150},
    
    // Bridge: 고음역 확장
    {GS2, 200}, {A2, 100}, {B2, 200}, {C2, 100},
    {D2_, 400}, {C2, 200}, {B2, 400}, {0, 200},
    
    // Chorus: 강렬한 리듬
    {E1, 100}, {E1, 100}, {F1, 200}, {GS1, 100},
    {A1, 100}, {GS1, 100}, {F1, 200}, {E1, 400},
    {D1_, 100}, {D1_, 100}, {C2, 200}, {B1, 100},
    {A1_, 100}, {GS1, 100}, {F1, 200}, {E1, 600},
    
    // Outro: 여운 처리
    {GS1, 800}, {A1, 400}, {E1, 1200}, {0, 200}
  };
  
  if((start) && (song_on))
  {
    start = 0;
    Buzzer_Beep(egyptian_start_song[0][0], egyptian_start_song[0][1]);//TIM3
    i = 0;
  }

  if(song_on)
  {
    if(n == (int)(egyptian_start_song[i][1]/10+0.5))
    {
      n = 0;
      if(i == (sizeof(egyptian_start_song)/sizeof(egyptian_start_song[0]) - 1))//노래가 종료된 경우
      {
        song_on = 0;
        i=0;
      }
      else
      {
        TIM3_Out_Stop();
        Buzzer_Beep(egyptian_start_song[i][0], egyptian_start_song[i][1]);//TIM3
      }
      i++;
    }
    n++;//음 길이용
  }
  else// song_on = 0;
  {
    TIM3_Out_Stop();
    i = 0;
    n = 0;
  }

   TIM4_expired = 1;
   Macro_Clear_Bit(TIM4->SR, 0);
 }

/*******************************************************************************
 * Function Name  : I2C1_EV_IRQHandler
 * Description    : This function handles I2C1 Event interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void I2C1_EV_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : I2C1_ER_IRQHandler
 * Description    : This function handles I2C1 Error interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void I2C1_ER_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : I2C2_EV_IRQHandler
 * Description    : This function handles I2C2 Event interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void I2C2_EV_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : I2C2_ER_IRQHandler
 * Description    : This function handles I2C2 Error interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void I2C2_ER_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : SPI1_IRQHandler
 * Description    : This function handles SPI1 global interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void SPI1_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : SPI2_IRQHandler
 * Description    : This function handles SPI2 global interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void SPI2_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : USART1_IRQHandler
 * Description    : This function handles USART1 global interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
 volatile int USART1_rx_ready = 0;
 volatile int USART1_rx_data;
 
 void USART1_IRQHandler(void)
 {
   USART1_rx_ready = 1;
   USART1_rx_data = Uart1_Get_Pressed();
 }

/*******************************************************************************
 * Function Name  : USART2_IRQHandler
 * Description    : This function handles USART2 global interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void USART2_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : USART3_IRQHandler
 * Description    : This function handles USART3 global interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void USART3_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : EXTI15_10_IRQHandler
 * Description    : This function handles External lines 15 to 10 interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
 void EXTI15_10_IRQHandler(void)
 {
   // 10
   static int EXTI15_10_LUT[4] = {0,4,5,0};
   Jog_key = EXTI15_10_LUT[Macro_Extract_Area(EXTI->PR, 0x3, 13)];
   Jog_key_in = 1;	
   EXTI->PR = 0x3<<13;
   NVIC_ClearPendingIRQ(EXTI15_10_IRQn);
 }

/*******************************************************************************
 * Function Name  : RTCAlarm_IRQHandler
 * Description    : This function handles RTC Alarm interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void RTCAlarm_IRQHandler(void)
{
  Invalid_ISR();
}

/*******************************************************************************
 * Function Name  : USBWakeUp_IRQHandler
 * Description    : This function handles USB WakeUp interrupt request.
 * Input          : None
 * Output         : None
 * Return         : None
 *******************************************************************************/
void USBWakeUp_IRQHandler(void)
{
  Invalid_ISR();
}

/******************* (C) COPYRIGHT 2008 STMicroelectronics *****END OF FILE****/
