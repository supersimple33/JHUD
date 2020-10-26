MAG_ADDRESS	= 0x1C	#Would be 0x1E if SDO_M is HIGH		
ACC_ADDRESS	= 0x6A  
GYR_ADDRESS = 0x6A  #Would be 0x6B if SDO_AG is HIGH

#/////////////////////////////////////////
#// LSM9DS1 Accel/Gyro (XL/G) Registers //
#/////////////////////////////////////////
ACT_THS				= 0x04
ACT_DUR				= 0x05
INT_GEN_CFG_XL		= 0x06
INT_GEN_THS_X_XL	= 0x07
INT_GEN_THS_Y_XL	= 0x08
INT_GEN_THS_Z_XL	= 0x09
INT_GEN_DUR_XL		= 0x0A
REFERENCE_G			= 0x0B
INT1_CTRL			= 0x0C
INT2_CTRL			= 0x0D
WHO_AM_I_XG			= 0x0F
CTRL_REG1_G			= 0x10
CTRL_REG2_G			= 0x11
CTRL_REG3_G			= 0x12
ORIENT_CFG_G		= 0x13
INT_GEN_SRC_G		= 0x14
OUT_TEMP_L			= 0x15
OUT_TEMP_H			= 0x16
STATUS_REG_0		= 0x17
OUT_X_L_G			= 0x18
OUT_X_H_G			= 0x19
OUT_Y_L_G			= 0x1A
OUT_Y_H_G			= 0x1B
OUT_Z_L_G			= 0x1C
OUT_Z_H_G			= 0x1D
CTRL_REG4			= 0x1E
CTRL_REG5_XL		= 0x1F
CTRL_REG6_XL		= 0x20
CTRL_REG7_XL		= 0x21
CTRL_REG8			= 0x22
CTRL_REG9			= 0x23
CTRL_REG10			= 0x24
INT_GEN_SRC_XL		= 0x26
STATUS_REG_1		= 0x27
OUT_X_L_XL			= 0x28
OUT_X_H_XL			= 0x29
OUT_Y_L_XL			= 0x2A
OUT_Y_H_XL			= 0x2B
OUT_Z_L_XL			= 0x2C
OUT_Z_H_XL			= 0x2D
FIFO_CTRL			= 0x2E
FIFO_SRC			= 0x2F
INT_GEN_CFG_G		= 0x30
INT_GEN_THS_XH_G	= 0x31
INT_GEN_THS_XL_G	= 0x32
INT_GEN_THS_YH_G	= 0x33
INT_GEN_THS_YL_G	= 0x34
INT_GEN_THS_ZH_G	= 0x35
INT_GEN_THS_ZL_G	= 0x36
INT_GEN_DUR_G		= 0x37

#///////////////////////////////
#// LSM9DS1 Magneto Registers //
#///////////////////////////////
OFFSET_X_REG_L_M	= 0x05
OFFSET_X_REG_H_M	= 0x06
OFFSET_Y_REG_L_M	= 0x07
OFFSET_Y_REG_H_M	= 0x08
OFFSET_Z_REG_L_M	= 0x09
OFFSET_Z_REG_H_M	= 0x0A
WHO_AM_I_M			= 0x0F
CTRL_REG1_M			= 0x20
CTRL_REG2_M			= 0x21
CTRL_REG3_M			= 0x22
CTRL_REG4_M			= 0x23
CTRL_REG5_M			= 0x24
STATUS_REG_M		= 0x27
OUT_X_L_M			= 0x28
OUT_X_H_M			= 0x29
OUT_Y_L_M			= 0x2A
OUT_Y_H_M			= 0x2B
OUT_Z_L_M			= 0x2C
OUT_Z_H_M			= 0x2D
INT_CFG_M			= 0x30
INT_SRC_M			= 0x30
INT_THS_L_M			= 0x32
INT_THS_H_M			= 0x33

#////////////////////////////////
#// LSM9DS1 WHO_AM_I Responses //
#////////////////////////////////
WHO_AM_I_AG_RSP		= 0x68
WHO_AM_I_M_RSP		= 0x3D