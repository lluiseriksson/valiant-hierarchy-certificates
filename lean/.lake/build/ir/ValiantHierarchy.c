// Lean compiler output
// Module: ValiantHierarchy
// Imports: public import Init public meta import Init
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_zPath3(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_zPath3___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_abpPath3(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_abpPath3___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__00(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__00___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__01(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__01___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__10(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__10___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__11(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__11___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_natListSum(lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_natListSum___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_zPath3(lean_object* v_x0_1_, lean_object* v_x1_2_, lean_object* v_m00_3_, lean_object* v_m01_4_, lean_object* v_m10_5_, lean_object* v_m11_6_, lean_object* v_z0_7_, lean_object* v_z1_8_){
_start:
{
lean_object* v___x_9_; lean_object* v___x_10_; lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_18_; lean_object* v___x_19_; 
v___x_9_ = lean_int_mul(v_x0_1_, v_m00_3_);
v___x_10_ = lean_int_mul(v___x_9_, v_z0_7_);
lean_dec(v___x_9_);
v___x_11_ = lean_int_mul(v_x0_1_, v_m01_4_);
v___x_12_ = lean_int_mul(v___x_11_, v_z1_8_);
lean_dec(v___x_11_);
v___x_13_ = lean_int_add(v___x_10_, v___x_12_);
lean_dec(v___x_12_);
lean_dec(v___x_10_);
v___x_14_ = lean_int_mul(v_x1_2_, v_m10_5_);
v___x_15_ = lean_int_mul(v___x_14_, v_z0_7_);
lean_dec(v___x_14_);
v___x_16_ = lean_int_add(v___x_13_, v___x_15_);
lean_dec(v___x_15_);
lean_dec(v___x_13_);
v___x_17_ = lean_int_mul(v_x1_2_, v_m11_6_);
v___x_18_ = lean_int_mul(v___x_17_, v_z1_8_);
lean_dec(v___x_17_);
v___x_19_ = lean_int_add(v___x_16_, v___x_18_);
lean_dec(v___x_18_);
lean_dec(v___x_16_);
return v___x_19_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_zPath3___boxed(lean_object* v_x0_20_, lean_object* v_x1_21_, lean_object* v_m00_22_, lean_object* v_m01_23_, lean_object* v_m10_24_, lean_object* v_m11_25_, lean_object* v_z0_26_, lean_object* v_z1_27_){
_start:
{
lean_object* v_res_28_; 
v_res_28_ = lp_valiant__hierarchy_ValiantHierarchy_zPath3(v_x0_20_, v_x1_21_, v_m00_22_, v_m01_23_, v_m10_24_, v_m11_25_, v_z0_26_, v_z1_27_);
lean_dec(v_z1_27_);
lean_dec(v_z0_26_);
lean_dec(v_m11_25_);
lean_dec(v_m10_24_);
lean_dec(v_m01_23_);
lean_dec(v_m00_22_);
lean_dec(v_x1_21_);
lean_dec(v_x0_20_);
return v_res_28_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_abpPath3(lean_object* v_x0_29_, lean_object* v_x1_30_, lean_object* v_m00_31_, lean_object* v_m01_32_, lean_object* v_m10_33_, lean_object* v_m11_34_, lean_object* v_z0_35_, lean_object* v_z1_36_){
_start:
{
lean_object* v___x_37_; lean_object* v___x_38_; lean_object* v___x_39_; lean_object* v___x_40_; lean_object* v___x_41_; lean_object* v___x_42_; lean_object* v___x_43_; lean_object* v___x_44_; lean_object* v___x_45_; 
v___x_37_ = lean_int_mul(v_x0_29_, v_m00_31_);
v___x_38_ = lean_int_mul(v_x1_30_, v_m10_33_);
v___x_39_ = lean_int_add(v___x_37_, v___x_38_);
lean_dec(v___x_38_);
lean_dec(v___x_37_);
v___x_40_ = lean_int_mul(v___x_39_, v_z0_35_);
lean_dec(v___x_39_);
v___x_41_ = lean_int_mul(v_x0_29_, v_m01_32_);
v___x_42_ = lean_int_mul(v_x1_30_, v_m11_34_);
v___x_43_ = lean_int_add(v___x_41_, v___x_42_);
lean_dec(v___x_42_);
lean_dec(v___x_41_);
v___x_44_ = lean_int_mul(v___x_43_, v_z1_36_);
lean_dec(v___x_43_);
v___x_45_ = lean_int_add(v___x_40_, v___x_44_);
lean_dec(v___x_44_);
lean_dec(v___x_40_);
return v___x_45_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_abpPath3___boxed(lean_object* v_x0_46_, lean_object* v_x1_47_, lean_object* v_m00_48_, lean_object* v_m01_49_, lean_object* v_m10_50_, lean_object* v_m11_51_, lean_object* v_z0_52_, lean_object* v_z1_53_){
_start:
{
lean_object* v_res_54_; 
v_res_54_ = lp_valiant__hierarchy_ValiantHierarchy_abpPath3(v_x0_46_, v_x1_47_, v_m00_48_, v_m01_49_, v_m10_50_, v_m11_51_, v_z0_52_, v_z1_53_);
lean_dec(v_z1_53_);
lean_dec(v_z0_52_);
lean_dec(v_m11_51_);
lean_dec(v_m10_50_);
lean_dec(v_m01_49_);
lean_dec(v_m00_48_);
lean_dec(v_x1_47_);
lean_dec(v_x0_46_);
return v_res_54_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__00(lean_object* v_a00_55_, lean_object* v_a01_56_, lean_object* v_b00_57_, lean_object* v_b10_58_){
_start:
{
lean_object* v___x_59_; lean_object* v___x_60_; lean_object* v___x_61_; 
v___x_59_ = lean_int_mul(v_a00_55_, v_b00_57_);
v___x_60_ = lean_int_mul(v_a01_56_, v_b10_58_);
v___x_61_ = lean_int_add(v___x_59_, v___x_60_);
lean_dec(v___x_60_);
lean_dec(v___x_59_);
return v___x_61_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__00___boxed(lean_object* v_a00_62_, lean_object* v_a01_63_, lean_object* v_b00_64_, lean_object* v_b10_65_){
_start:
{
lean_object* v_res_66_; 
v_res_66_ = lp_valiant__hierarchy_ValiantHierarchy_mul2__00(v_a00_62_, v_a01_63_, v_b00_64_, v_b10_65_);
lean_dec(v_b10_65_);
lean_dec(v_b00_64_);
lean_dec(v_a01_63_);
lean_dec(v_a00_62_);
return v_res_66_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__01(lean_object* v_a00_67_, lean_object* v_a01_68_, lean_object* v_b01_69_, lean_object* v_b11_70_){
_start:
{
lean_object* v___x_71_; lean_object* v___x_72_; lean_object* v___x_73_; 
v___x_71_ = lean_int_mul(v_a00_67_, v_b01_69_);
v___x_72_ = lean_int_mul(v_a01_68_, v_b11_70_);
v___x_73_ = lean_int_add(v___x_71_, v___x_72_);
lean_dec(v___x_72_);
lean_dec(v___x_71_);
return v___x_73_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__01___boxed(lean_object* v_a00_74_, lean_object* v_a01_75_, lean_object* v_b01_76_, lean_object* v_b11_77_){
_start:
{
lean_object* v_res_78_; 
v_res_78_ = lp_valiant__hierarchy_ValiantHierarchy_mul2__01(v_a00_74_, v_a01_75_, v_b01_76_, v_b11_77_);
lean_dec(v_b11_77_);
lean_dec(v_b01_76_);
lean_dec(v_a01_75_);
lean_dec(v_a00_74_);
return v_res_78_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__10(lean_object* v_a10_79_, lean_object* v_a11_80_, lean_object* v_b00_81_, lean_object* v_b10_82_){
_start:
{
lean_object* v___x_83_; lean_object* v___x_84_; lean_object* v___x_85_; 
v___x_83_ = lean_int_mul(v_a10_79_, v_b00_81_);
v___x_84_ = lean_int_mul(v_a11_80_, v_b10_82_);
v___x_85_ = lean_int_add(v___x_83_, v___x_84_);
lean_dec(v___x_84_);
lean_dec(v___x_83_);
return v___x_85_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__10___boxed(lean_object* v_a10_86_, lean_object* v_a11_87_, lean_object* v_b00_88_, lean_object* v_b10_89_){
_start:
{
lean_object* v_res_90_; 
v_res_90_ = lp_valiant__hierarchy_ValiantHierarchy_mul2__10(v_a10_86_, v_a11_87_, v_b00_88_, v_b10_89_);
lean_dec(v_b10_89_);
lean_dec(v_b00_88_);
lean_dec(v_a11_87_);
lean_dec(v_a10_86_);
return v_res_90_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__11(lean_object* v_a10_91_, lean_object* v_a11_92_, lean_object* v_b01_93_, lean_object* v_b11_94_){
_start:
{
lean_object* v___x_95_; lean_object* v___x_96_; lean_object* v___x_97_; 
v___x_95_ = lean_int_mul(v_a10_91_, v_b01_93_);
v___x_96_ = lean_int_mul(v_a11_92_, v_b11_94_);
v___x_97_ = lean_int_add(v___x_95_, v___x_96_);
lean_dec(v___x_96_);
lean_dec(v___x_95_);
return v___x_97_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_mul2__11___boxed(lean_object* v_a10_98_, lean_object* v_a11_99_, lean_object* v_b01_100_, lean_object* v_b11_101_){
_start:
{
lean_object* v_res_102_; 
v_res_102_ = lp_valiant__hierarchy_ValiantHierarchy_mul2__11(v_a10_98_, v_a11_99_, v_b01_100_, v_b11_101_);
lean_dec(v_b11_101_);
lean_dec(v_b01_100_);
lean_dec(v_a11_99_);
lean_dec(v_a10_98_);
return v_res_102_;
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_natListSum(lean_object* v_x_103_){
_start:
{
if (lean_obj_tag(v_x_103_) == 0)
{
lean_object* v___x_104_; 
v___x_104_ = lean_unsigned_to_nat(0u);
return v___x_104_;
}
else
{
lean_object* v_head_105_; lean_object* v_tail_106_; lean_object* v___x_107_; lean_object* v___x_108_; 
v_head_105_ = lean_ctor_get(v_x_103_, 0);
v_tail_106_ = lean_ctor_get(v_x_103_, 1);
v___x_107_ = lp_valiant__hierarchy_ValiantHierarchy_natListSum(v_tail_106_);
v___x_108_ = lean_nat_add(v_head_105_, v___x_107_);
lean_dec(v___x_107_);
return v___x_108_;
}
}
}
LEAN_EXPORT lean_object* lp_valiant__hierarchy_ValiantHierarchy_natListSum___boxed(lean_object* v_x_109_){
_start:
{
lean_object* v_res_110_; 
v_res_110_ = lp_valiant__hierarchy_ValiantHierarchy_natListSum(v_x_109_);
lean_dec(v_x_109_);
return v_res_110_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
void lean_initialize_runtime_module();
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_valiant__hierarchy_ValiantHierarchy(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
lean_initialize_runtime_module();
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
