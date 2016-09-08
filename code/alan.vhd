library ieee;
use ieee.std_logic_1164.ALL;

library UNISIM;
use UNISIM.VComponents.all;

library work ;
use work.logi_wishbone_pack.all ;
use work.logi_wishbone_peripherals_pack.all ;


entity alan is
	port(
		OSC_FPGA : in std_logic ;
		MOSI :  in std_logic;
		MISO :   out  std_logic;
		SS :  in std_logic;
		SCK :  in std_logic;
		LED :   out  std_logic_vector((2-1) downto 0);
		PMOD1 :   inout  std_logic_vector((8-1) downto 0);
		PMOD2 :   inout  std_logic_vector((8-1) downto 0);
		PMOD3 :   inout  std_logic_vector((8-1) downto 0);
		PMOD4 :   inout  std_logic_vector((8-1) downto 0);
		ARD :   inout  std_logic_vector((6-1) downto 0);
		PB :  in std_logic_vector((2-1) downto 0);
		SW :  in std_logic_vector((2-1) downto 0)
	);
end alan;

architecture structural of alan is

	type wishbone_bus is
	record
		address : std_logic_vector(15 downto 0);
		writedata : std_logic_vector(15 downto 0);
		readdata : std_logic_vector(15 downto 0);
		cycle: std_logic;
		write : std_logic;
		strobe : std_logic;
		ack : std_logic;
	end record;

	signal gls_clk, gls_reset, clk_locked, osc_buff, clkfb : std_logic ;

	signal Master_0_wbm_Intercon_0_wbs_0 : wishbone_bus;
	signal top_MOSI_Master_0_mosi_0 : std_logic;
	signal top_SS_Master_0_ss_0 : std_logic;
	signal top_SCK_Master_0_sck_0 : std_logic;
	signal Master_0_miso_top_MISO_0 : std_logic;
	signal Intercon_0_wbm_PWM_0_wbs_0 : wishbone_bus;
	signal PWM_0_pwm_out_top_LED_0 : std_logic;
	signal Intercon_0_wbm_reg_checksum_wbs_0 : wishbone_bus;
	signal Intercon_0_wbm_reg_errorchecck_wbs_0 : wishbone_bus;

begin


gls_reset <= (NOT clk_locked); -- system reset while clock not locked



Master_0 : spi_wishbone_wrapper
-- no generics
port map(
	gls_clk => gls_clk, gls_reset => gls_reset,

	mosi =>  top_MOSI_Master_0_mosi_0,

	miso =>  Master_0_miso_top_MISO_0,

	ss =>  top_SS_Master_0_ss_0,

	sck =>  top_SCK_Master_0_sck_0,

	wbm_address =>  Master_0_wbm_Intercon_0_wbs_0.address,
	wbm_writedata =>  Master_0_wbm_Intercon_0_wbs_0.writedata,
	wbm_readdata =>  Master_0_wbm_Intercon_0_wbs_0.readdata,
	wbm_cycle =>  Master_0_wbm_Intercon_0_wbs_0.cycle,
	wbm_strobe =>  Master_0_wbm_Intercon_0_wbs_0.strobe,
	wbm_write =>  Master_0_wbm_Intercon_0_wbs_0.write,
	wbm_ack =>  Master_0_wbm_Intercon_0_wbs_0.ack
);

Intercon_0 : wishbone_intercon
generic map(
memory_map => ("000000000001XXXX", "0000000000000000", "0000000000010001")
)
port map(
	gls_clk => gls_clk, gls_reset => gls_reset,

	wbs_address =>  Master_0_wbm_Intercon_0_wbs_0.address,
	wbs_writedata =>  Master_0_wbm_Intercon_0_wbs_0.writedata,
	wbs_readdata =>  Master_0_wbm_Intercon_0_wbs_0.readdata,
	wbs_cycle =>  Master_0_wbm_Intercon_0_wbs_0.cycle,
	wbs_strobe =>  Master_0_wbm_Intercon_0_wbs_0.strobe,
	wbs_write =>  Master_0_wbm_Intercon_0_wbs_0.write,
	wbs_ack =>  Master_0_wbm_Intercon_0_wbs_0.ack,

	wbm_address(0) =>  Intercon_0_wbm_PWM_0_wbs_0.address,
		wbm_address(1) =>  Intercon_0_wbm_reg_checksum_wbs_0.address,
		wbm_address(2) =>  Intercon_0_wbm_reg_errorchecck_wbs_0.address,
	wbm_writedata(0) =>  Intercon_0_wbm_PWM_0_wbs_0.writedata,
		wbm_writedata(1) =>  Intercon_0_wbm_reg_checksum_wbs_0.writedata,
		wbm_writedata(2) =>  Intercon_0_wbm_reg_errorchecck_wbs_0.writedata,
	wbm_readdata(0) =>  Intercon_0_wbm_PWM_0_wbs_0.readdata,
		wbm_readdata(1) =>  Intercon_0_wbm_reg_checksum_wbs_0.readdata,
		wbm_readdata(2) =>  Intercon_0_wbm_reg_errorchecck_wbs_0.readdata,
	wbm_cycle(0) =>  Intercon_0_wbm_PWM_0_wbs_0.cycle,
		wbm_cycle(1) =>  Intercon_0_wbm_reg_checksum_wbs_0.cycle,
		wbm_cycle(2) =>  Intercon_0_wbm_reg_errorchecck_wbs_0.cycle,
	wbm_strobe(0) =>  Intercon_0_wbm_PWM_0_wbs_0.strobe,
		wbm_strobe(1) =>  Intercon_0_wbm_reg_checksum_wbs_0.strobe,
		wbm_strobe(2) =>  Intercon_0_wbm_reg_errorchecck_wbs_0.strobe,
	wbm_write(0) =>  Intercon_0_wbm_PWM_0_wbs_0.write,
		wbm_write(1) =>  Intercon_0_wbm_reg_checksum_wbs_0.write,
		wbm_write(2) =>  Intercon_0_wbm_reg_errorchecck_wbs_0.write,
	wbm_ack(0) =>  Intercon_0_wbm_PWM_0_wbs_0.ack,
		wbm_ack(1) =>  Intercon_0_wbm_reg_checksum_wbs_0.ack,
		wbm_ack(2) =>  Intercon_0_wbm_reg_errorchecck_wbs_0.ack
);

PWM_0 : wishbone_pwm
generic map(
nb_chan => 7
)
port map(
	gls_clk => gls_clk, gls_reset => gls_reset,

	wbs_address =>  Intercon_0_wbm_PWM_0_wbs_0.address,
	wbs_writedata =>  Intercon_0_wbm_PWM_0_wbs_0.writedata,
	wbs_readdata =>  Intercon_0_wbm_PWM_0_wbs_0.readdata,
	wbs_cycle =>  Intercon_0_wbm_PWM_0_wbs_0.cycle,
	wbs_strobe =>  Intercon_0_wbm_PWM_0_wbs_0.strobe,
	wbs_write =>  Intercon_0_wbm_PWM_0_wbs_0.write,
	wbs_ack =>  Intercon_0_wbm_PWM_0_wbs_0.ack,

	pwm_out(0) =>  PWM_0_pwm_out_top_LED_0,
	pwm_out(6 downto 1) => open
);

reg_checksum : wishbone_register
generic map(
nb_regs => 1
)

port map(
	gls_clk => gls_clk, gls_reset => gls_reset,

	wbs_address =>  Intercon_0_wbm_reg_checksum_wbs_0.address,
	wbs_writedata =>  Intercon_0_wbm_reg_checksum_wbs_0.writedata,
	wbs_readdata =>  Intercon_0_wbm_reg_checksum_wbs_0.readdata,
	wbs_cycle =>  Intercon_0_wbm_reg_checksum_wbs_0.cycle,
	wbs_strobe =>  Intercon_0_wbm_reg_checksum_wbs_0.strobe,
	wbs_write =>  Intercon_0_wbm_reg_checksum_wbs_0.write,
	wbs_ack =>  Intercon_0_wbm_reg_checksum_wbs_0.ack,

	reg_out(0)(15 downto 0) => open,

	reg_in(0)(15 downto 0) => (others => '0')
);
signal_input<=signal_input+reg_in(0) & 00000000 << 2
PMOD2(7 downto 0) <= signal_output(15 downto 8);
PMOD1(7 downto 0) <= signal_output(7 downto 0);

reg_errorchecck : wishbone_register
generic map(
nb_regs => 1
)
port map(
	gls_clk => gls_clk, gls_reset => gls_reset,

	wbs_address =>  Intercon_0_wbm_reg_errorchecck_wbs_0.address,
	wbs_writedata =>  Intercon_0_wbm_reg_errorchecck_wbs_0.writedata,
	wbs_readdata =>  Intercon_0_wbm_reg_errorchecck_wbs_0.readdata,
	wbs_cycle =>  Intercon_0_wbm_reg_errorchecck_wbs_0.cycle,
	wbs_strobe =>  Intercon_0_wbm_reg_errorchecck_wbs_0.strobe,
	wbs_write =>  Intercon_0_wbm_reg_errorchecck_wbs_0.write,
	wbs_ack =>  Intercon_0_wbm_reg_errorchecck_wbs_0.ack,

	reg_out(0)(15 downto 0) => open,

	reg_in(0)(15 downto 0) => (others => '0')
);
signal_input = signal_input+reg_in(0)
PMOD2(7 downto 0) <= signal_output(15 downto 8);
PMOD1(7 downto 0) <= signal_output(7 downto 0); 

-- Connecting inputs
top_MOSI_Master_0_mosi_0 <= MOSI;
top_SS_Master_0_ss_0 <= SS;
top_SCK_Master_0_sck_0 <= SCK;
-- <= PB;
-- <= SW;

-- Connecting outputs
MISO <= Master_0_miso_top_MISO_0;
LED(0) <= PWM_0_pwm_out_top_LED_0;
LED(1) <= 'Z';

-- Connecting inouts

PMOD1(7 downto 0) <= (others => 'Z');
--(others => 'Z') <= PMOD1(7 downto 0);


PMOD2(7 downto 0) <= (others => 'Z');
--(others => 'Z') <= PMOD2(7 downto 0);


PMOD3(7 downto 0) <= (others => 'Z');
--(others => 'Z') <= PMOD3(7 downto 0);


PMOD4(7 downto 0) <= (others => 'Z');
--(others => 'Z') <= PMOD4(7 downto 0);


ARD(5 downto 0) <= (others => 'Z');
--(others => 'Z') <= ARD(5 downto 0);






-- system clock generation

PLL_BASE_inst : PLL_BASE generic map (
      BANDWIDTH      => "OPTIMIZED",        -- "HIGH", "LOW" or "OPTIMIZED"
      CLKFBOUT_MULT  => 16 ,                 -- Multiply value for all CLKOUT clock outputs (1-64)
      CLKFBOUT_PHASE => 0.0,                -- Phase offset in degrees of the clock feedback output (0.0-360.0).
      CLKIN_PERIOD   => 20.00,              -- Input clock period in ns to ps resolution (i.e. 33.333 is 30 MHz).
      -- CLKOUT0_DIVIDE - CLKOUT5_DIVIDE: Divide amount for CLKOUT# clock output (1-128)
      CLKOUT0_DIVIDE => 8,       CLKOUT1_DIVIDE => 1,
      CLKOUT2_DIVIDE => 1,       CLKOUT3_DIVIDE => 1,
      CLKOUT4_DIVIDE => 1,       CLKOUT5_DIVIDE => 1,
      -- CLKOUT0_DUTY_CYCLE - CLKOUT5_DUTY_CYCLE: Duty cycle for CLKOUT# clock output (0.01-0.99).
      CLKOUT0_DUTY_CYCLE => 0.5, CLKOUT1_DUTY_CYCLE => 0.5,
      CLKOUT2_DUTY_CYCLE => 0.5, CLKOUT3_DUTY_CYCLE => 0.5,
      CLKOUT4_DUTY_CYCLE => 0.5, CLKOUT5_DUTY_CYCLE => 0.5,
      -- CLKOUT0_PHASE - CLKOUT5_PHASE: Output phase relationship for CLKOUT# clock output (-360.0-360.0).
      CLKOUT0_PHASE => 0.0,      CLKOUT1_PHASE => 0.0, -- Capture clock
      CLKOUT2_PHASE => 0.0,      CLKOUT3_PHASE => 0.0,
      CLKOUT4_PHASE => 0.0,      CLKOUT5_PHASE => 0.0,

      CLK_FEEDBACK => "CLKFBOUT",           -- Clock source to drive CLKFBIN ("CLKFBOUT" or "CLKOUT0")
      COMPENSATION => "SYSTEM_SYNCHRONOUS", -- "SYSTEM_SYNCHRONOUS", "SOURCE_SYNCHRONOUS", "EXTERNAL"
      DIVCLK_DIVIDE => 1,                   -- Division value for all output clocks (1-52)
      REF_JITTER => 0.1,                    -- Reference Clock Jitter in UI (0.000-0.999).
      RESET_ON_LOSS_OF_LOCK => FALSE        -- Must be set to FALSE
   ) port map (
      CLKFBOUT => clkfb, -- 1-bit output: PLL_BASE feedback output
      -- CLKOUT0 - CLKOUT5: 1-bit (each) output: Clock outputs
      CLKOUT0 => gls_clk,      CLKOUT1 => open,
      CLKOUT2 => open,      CLKOUT3 => open,
      CLKOUT4 => open,      CLKOUT5 => open,
      LOCKED  => clk_locked,  -- 1-bit output: PLL_BASE lock status output
      CLKFBIN => clkfb, -- 1-bit input: Feedback clock input
      CLKIN   => osc_buff,  -- 1-bit input: Clock input
      RST     => '0'    -- 1-bit input: Reset input
   );

    -- Buffering of clocks
	BUFG_1 : BUFG port map (O => osc_buff,    I => OSC_FPGA);

end structural ;
