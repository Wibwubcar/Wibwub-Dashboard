
// ════════════════════════════════════════
// RAW DATA
// ════════════════════════════════════════
const M5 = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.","ก.ย."];
// วันสุดท้ายของข้อมูลยอดขายที่ซิงก์แล้ว (เดือนล่าสุดใน M5 = MTD ถึงวันนี้)
// ทุก label ที่พูดถึง "ข้อมูลถึงวันที่" ให้ derive จากตรงนี้ ห้าม hardcode ซ้ำ
// (ดู skill: wibwub-avoid-stale-hardcoded-labels)
const SALES_ASOF = '2026-09-20';
function salesAsofTH(){
  const TH=['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.'];
  const p=SALES_ASOF.split('-');
  return `${+p[2]} ${TH[+p[1]-1]} ${+p[0]+543}`;
}
function salesRangeTH(){ return `ม.ค. – ${M5[M5.length-1]} ${new Date(SALES_ASOF).getFullYear()+543}`; }
function salesPartialNote(){
  const p=SALES_ASOF.split('-');
  return `* ${M5[M5.length-1]} ${+p[0]+543} เป็นข้อมูลบางส่วน (1–${+p[2]} ${M5[M5.length-1]})`;
}
const SH_REV=[4231653,4383214,4560321,5204395,5581064,5632009,5923704,6604604,3326267];
const TK_REV=[1152566.73,1171209.0,1280967.0,1350396.99,1563644.02,1167356.96,2089005.47,2522656.21,2154005.46];
const LZ_REV=[179084,120948,183370,110531,129523,118094.7,95770.98,119349.79,59719.97];
const FB_REV=[2152231,1328934,1061901,802047,980883,413040,413040,413040,413040];
const LINE_REV=[350828,459158,418472,397898,374817,153907,153907,153907,153907];
const WEB_REV=[4568,1760,11754,3060,4468,1355,1355,1355,1355];
const CARE_REV=[84069,90135,70707,92509,98307,0,0,0,0];
const MKT_REV=[580,0,0,490,17365,0,0,0,0];
const BEUK_REV=[0,0,0,0,365,0,0,0,0];
const POS_REV=[435,548,2277,267,590,0,0,0,0];
const SH_ORD=[7532,6580,6873,8128,9093,8895,10511,11689,5857];
const TK_ORD=[3204,3652,3934,5032,7543,4260,10094,11498,9826];
const LZ_ORD=[236,176,255,161,157,158,146,146,146];
const FB_ORD=[2987,2001,1575,1175,1479,649,649,649,649];
const LINE_ORD=[325,466,345,381,343,152,152,152,152];
const SH_CANCEL=[4.62,4.45,4.26,5.94,5.38,5.16,5.34,5.89,5.53];
const TK_CANCEL=[9.64,8.32,8.39,9.7,7.69,8.45,7.55,6.53,6.63];
const LZ_CANCEL=[16.1,18.2,20.8,20.5,20.38,13.92,21.92,21.92,21.92];
// SH_ADS = ค่าโฆษณา/การตลาด Shopee ทั้งหมดจาก Google Sheet (sales sync) — กว้างกว่ารายงาน Shopee Ads portal
// ห้าม overwrite ด้วยยอด spend จาก Shopee Ads report (ส.ค. 2569: Sheet 1,185,609.37 vs Ads report 974,764.42)
// index อ้างอิง array M5 ซึ่งเดือนสุดท้ายเป็น MTD (วันสุดท้ายจริงดู SALES_ASOF / salesAsofTH()) — เดือนถัดไปจะเพิ่มเมื่อ sales sync มีข้อมูล
const SH_ADS=[575400,559100,589300,795300,826300,885100,942122.40,1185609.37,714615.75];
const SH_FEE=[911498,944144,1046921,1225115,1433217,1506562,1774741.72,1978739.36,996549.59];
const TK_ADSSPEND = [164956,202579,249294,256168,357295,249628,508456,682200,578702.47];
const TK_FEECOMM = [271216,267255,270719,294223,402802,291455,613482,742365,641658.79];
const TK_AFI=[460976,550756,655259,724120,948916,642235,1453863,1526564,1140248.32];
const TK_NET=[456036,544073,642947,708730,934535,632058,1429605,1502415,1122613.16];
const LZ_CANCEL_PCT=[16.1,18.2,20.8,20.5,20.38,13.92,21.92,21.92,21.92];
const LZ_COST_PCT=[22.67,24.61,24.36,24.86,25.0,26.34,30.99,29.67,28.73];
const LZ_ADS=[5760,5680,7220,5710,6590,8420,9710,11333,3470];
const TOTAL_REV = SH_REV.map((_,i)=>SH_REV[i]+TK_REV[i]+LZ_REV[i]+FB_REV[i]+LINE_REV[i]+WEB_REV[i]+CARE_REV[i]+MKT_REV[i]+BEUK_REV[i]+POS_REV[i]);
const TOTAL_ORD = SH_ORD.map((_,i)=>SH_ORD[i]+TK_ORD[i]+LZ_ORD[i]+FB_ORD[i]+LINE_ORD[i]);

const CHANNELS=[
  {n:'Shopee',v:35516360,color:'#ee4d2d'},
  {n:'TikTok',v:9775146,color:'#111'},
  {n:'Facebook',v:6739036,color:'#1877f2'},
  {n:'Line Shopping',v:2155080,color:'#06c755'},
  {n:'Lazada',v:937322,color:'#1b04a1'},
  {n:'Website/อื่นๆ',v:28320,color:'#1A5CDB'},
];

const AFI_MONTHS=['พย.68','ธค.68','มค.69','กพ.69','มีนา.69','เมษา.69','พค.69','มิย.69','กค.69 (1-31)','สค.69 (1-31)','กย.69 (1-19)'];
const AFI_GMV=[0,0,0,0,655171,724241,951158,660557,1452748,1730666,1334642];
const AFI_NET=[0,0,0,0,642865,708855,937203,650042,1428498,1701769,1241216];
const AFI_COMM=[0,0,0,0,82699,69021,104772,79293,169224,198783,146703];
const TK_FOL = [23404,24192,24967,25590,26339,27083,27834,28684,29594];
const FOL_M=['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.'];

const CREATORS=[
  {n:"rita.fe_",t:416989,ma:8,mn:[14796,54474,72545,72993,75273,60628,41704,24576]},
  {n:"fahareejun",t:274047,ma:3,mn:[null,null,null,null,null,29331,226977,17739]},
  {n:"pailong05",t:193688,ma:4,mn:[null,null,null,null,14830,66465,73180,39213]},
  {n:"noonjourneyyy",t:190271,ma:5,mn:[null,null,null,41441,35232,44277,35765,33556]},
  {n:"jarkkystory",t:161816,ma:8,mn:[7350,21237,31167,20819,30903,23146,13688,13506]},
  {n:"muchmai_mumi",t:144518,ma:8,mn:[558,397,5796,43002,31897,26324,22223,14321]},
  {n:"ralph.detailing8",t:120763,ma:8,mn:[2083,7237,16427,14622,19175,20651,25330,15238]},
  {n:"phanuwatinsri",t:114223,ma:8,mn:[18313,8637,9019,10956,20766,18078,18646,9808]},
  {n:"thekataecx30",t:98778,ma:7,mn:[34551,3339,6362,12485,9705,21577,10759,null]},
  {n:"rrak_kk",t:88275,ma:8,mn:[11014,2483,5207,9853,14409,16555,13092,15662]},
  {n:"nnhtr_",t:82929,ma:4,mn:[null,null,null,null,14249,23872,28702,16106]},
  {n:"melodylotto",t:82562,ma:8,mn:[8444,8691,11160,7484,13029,14705,9800,9249]},
  {n:"evee.vespa",t:79462,ma:8,mn:[6275,14392,13337,12095,10592,8992,8597,5182]},
  {n:"_ijstagram",t:75088,ma:7,mn:[4331,6977,4183,10465,13609,20833,14690,null]},
  {n:"papajate",t:73829,ma:5,mn:[null,null,null,8105,10417,7891,16425,30991]},
  {n:"orion_risingstar",t:70522,ma:5,mn:[null,null,null,8448,15588,14461,19517,12508]},
  {n:"plearntumarai",t:65976,ma:5,mn:[null,null,null,6852,12638,19349,18841,8296]},
  {n:"taaum234",t:63092,ma:8,mn:[24010,2761,2941,8807,13900,5533,2823,2317]},
  {n:".namoshop125",t:62429,ma:1,mn:[null,null,null,null,null,null,null,62429]},
  {n:"jaonnm",t:56989,ma:4,mn:[13443,13185,12961,17400,null,null,null,null]},
  {n:"mushinyiwz",t:52910,ma:6,mn:[null,null,15490,20745,9265,1341,2123,3946]},
  {n:"numtonn",t:45033,ma:6,mn:[null,null,2297,21832,5030,10405,3991,1478]},
  {n:"punch_chalita8",t:44146,ma:8,mn:[431,5065,10375,2940,6923,9383,3940,5089]},
  {n:"rouey_sook",t:39798,ma:8,mn:[5946,8699,11963,2887,4313,1740,2201,2049]},
  {n:"phuengthitii",t:35817,ma:2,mn:[null,null,null,null,null,null,27516,8301]},
  {n:"ploypimlaplus",t:34902,ma:8,mn:[1179,486,2563,3943,8308,9800,7918,705]},
  {n:"ceo.blk.item",t:34446,ma:3,mn:[null,null,null,null,null,5957,26234,2255]},
  {n:"poppyme.6",t:33717,ma:4,mn:[null,null,null,null,13386,10912,8787,632]},
  {n:"tonpalm__",t:26988,ma:6,mn:[2633,9392,7903,3649,2207,1204,null,null]},
  {n:"somkidkongchom",t:26830,ma:5,mn:[null,null,null,417,2476,5887,6520,11530]},
  {n:"ctl.mkzk",t:26452,ma:8,mn:[5219,2909,4004,4141,3178,3554,1838,1609]},
  {n:"joakrw",t:23337,ma:8,mn:[4490,648,1293,3460,2922,1290,5913,3321]},
  {n:"japann.story",t:21394,ma:8,mn:[2539,2709,5143,2947,1162,3130,2323,1441]},
  {n:"aoohphonhan",t:20968,ma:7,mn:[337,277,2958,null,6277,5878,2864,2377]},
  {n:"tangkwaky",t:20519,ma:7,mn:[null,1108,3806,3570,2461,3115,2603,3856]},
  {n:"manutsananpibanwo",t:20154,ma:7,mn:[237,4973,6942,1284,4354,1100,null,1264]},
  {n:"rawinreview2465",t:18530,ma:4,mn:[null,null,null,null,2204,3724,12010,592]},
  {n:"calvyn.s",t:18324,ma:7,mn:[1320,1537,6621,2973,2830,1410,null,1633]},
  {n:"duan4088",t:17765,ma:5,mn:[135,11352,6050,134,null,null,null,94]},
  {n:"iceshop45_",t:16189,ma:8,mn:[2906,4581,2416,1472,2430,862,661,861]},
  {n:"teetathlimchuwong",t:15335,ma:6,mn:[null,null,390,7969,3806,1139,1193,838]},
  {n:"aornor.kd",t:15248,ma:6,mn:[null,null,1286,2328,1525,2260,5016,2833]},
  {n:"body.chaya9",t:14445,ma:4,mn:[null,null,null,null,2412,3146,2813,6074]},
  {n:"krunid_",t:13495,ma:6,mn:[3986,2140,2653,2530,1556,null,null,630]},
  {n:"sleepreview",t:13462,ma:7,mn:[null,1470,2463,390,1500,3269,2986,1384]},
  {n:"saiinum.storry",t:13092,ma:2,mn:[null,null,null,null,null,null,3424,9668]},
  {n:"james.khunphrom",t:11833,ma:7,mn:[693,158,490,758,780,null,4680,4274]},
  {n:"view.miipro",t:11831,ma:5,mn:[null,1388,7264,1140,1046,993,null,0]},
  {n:"eiwvanilla",t:11625,ma:6,mn:[1594,575,2158,2276,3952,null,null,1070]},
  {n:"suwit_deepal.khonkaen",t:11389,ma:6,mn:[null,79,null,199,2555,2912,3840,1804]}
];


// Top 15 products cumulative ม.ค.–ก.ย. (data through 18.09, updated 18.09.69 Monday-run)
// v=ยอดขายจริง (เฉพาะแถวที่ราคา>0), q=จำนวนจริง, mk=งบการตลาด(ของแจก/ส่งInfluencer), mkq=จำนวนงบตลาด — mk/mkq carried over from prior run, not recomputed this run
// grouping = SKU หลัก + ชื่อ listing ภาษาอื่น/ชื่อการตลาดของสินค้าเดียวกัน (ขนาด 3L/5L นับแยกกลุ่ม)
// 18.09.69: เพิ่มเฉพาะยอด 18 ก.ย. (บางส่วน, ดึงข้อมูล 02:55 น.) ทับยอดเดิมถึง 17 ก.ย. — ยังไม่ recompute ย้อนหลัง ม.ค.–ส.ค.
const ALL_PRODUCTS = [
  {n:'Sugar สเปรย์แวกซ์เคลือบสีรถ', v:6448007, q:20911, mk:53448, mkq:192},
  {n:'Wool Duster ไม้ปัดฝุ่นขนแกะ', v:6167016, q:9690, mk:13188, mkq:20},
  {n:'Interior สเปรย์ทำความสะอาดภายในรถ', v:4604108, q:13253, mk:69555, mkq:189},
  {n:'Refresh Wipes ทิชชู่เปียกเบาะหนัง', v:3792639, q:47955, mk:17966, mkq:231},
  {n:'Interior Wipe ทิชชู่เปียกภายในรถ', v:3204337, q:43654, mk:12923, mkq:167},
  {n:'Refresh สเปรย์โฟมทำความสะอาด', v:2738739, q:7624, mk:19955, mkq:52},
  {n:'Spot Clean น้ำยาขจัดคราบน้ำ', v:2659109, q:7016, mk:5982, mkq:16},
  {n:'Perfect ผ้าไมโครไฟเบอร์ BOA 500gsm', v:2089484, q:13607, mk:25870, mkq:159},
  {n:'Reflex Ceramic Coating สเปรย์เคลือบสี', v:1848716, q:4776, mk:12916, mkq:34},
  {n:'X-Glass Shield น้ำยาเคลือบกระจก', v:1738542, q:4674, mk:11341, mkq:30},
  {n:'Tire & Trim เจลเคลือบพลาสติกและยาง', v:1732658, q:3784, mk:10959, mkq:27},
  {n:'Martini ผ้าเช็ดน้ำยาเคลือบสี', v:1645093, q:13003, mk:17721, mkq:150},
  {n:'Sugar สเปรย์แวกซ์ขนาด 3L', v:1621028, q:1355, mk:2100, mkq:2},
  {n:'Quartz Shampoo น้ำยาล้างรถ 1L', v:1517158, q:6251, mk:8001, mkq:46},
  {n:'Reflex Ceramic Coating ขนาด 500ml', v:1430247, q:2204, mk:1240, mkq:2},
];
// Per-month product revenue [Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep(1-18)] — Shipnity ม.ค.–18 ก.ย. 2569
const PROD_MO=[
  {n:'Wool Duster ไม้ปัดฝุ่นขนแกะ', mo:[1495083, 1041074, 981641, 788587, 489154, 377935, 395560, 387491, 210491]},
  {n:'Sugar สเปรย์แวกซ์เคลือบสีรถ', mo:[822778, 670653, 606708, 561482, 549210, 654003, 786289, 954701, 842183]},
  {n:'Interior สเปรย์ทำความสะอาดภายในรถ', mo:[568676, 450756, 470790, 523676, 528615, 496317, 570884, 642301, 352093]},
  {n:'Refresh Wipes ทิชชู่เปียกเบาะหนัง', mo:[141707, 134280, 166974, 269674, 548615, 112236, 680786, 1080875, 657492]},
  {n:'Interior Wipe ทิชชู่เปียกภายในรถ', mo:[193960, 206324, 237744, 332049, 406740, 329010, 574434, 582559, 341517]},
  {n:'Refresh สเปรย์โฟมทำความสะอาด', mo:[293360, 245303, 282205, 306164, 307133, 321368, 389250, 384984, 208972]},
  {n:'Spot Clean น้ำยาขจัดคราบน้ำ', mo:[177233, 132568, 116783, 305741, 394366, 445551, 384962, 441636, 260269]},
  {n:'Perfect ผ้าไมโครไฟเบอร์ BOA 500gsm', mo:[370067, 274978, 234139, 216089, 228141, 197725, 192362, 232539, 143444]},
  {n:'Reflex Ceramic Coating สเปรย์เคลือบสี', mo:[288877, 286316, 229188, 173243, 159182, 193221, 172197, 196720, 149772]},
  {n:'X-Glass Shield น้ำยาเคลือบกระจก', mo:[109063, 92404, 75284, 81349, 274389, 384199, 277431, 258546, 185877]},
  {n:'Tire & Trim เจลเคลือบพลาสติกและยาง', mo:[249084, 188838, 158145, 193075, 192518, 181928, 193008, 225100, 150962]},
  {n:'Martini ผ้าเช็ดน้ำยาเคลือบสี', mo:[239590, 175122, 147407, 147097, 190038, 203261, 205973, 211763, 124842]},
  {n:'Sugar สเปรย์แวกซ์ขนาด 3L', mo:[297428, 201858, 148678, 176607, 177593, 181012, 162710, 168129, 107013]},
  {n:'Quartz Shampoo น้ำยาล้างรถ 1L', mo:[203130, 161032, 149829, 150665, 187402, 161194, 171319, 198541, 134046]},
  {n:'Reflex Ceramic Coating ขนาด 500ml', mo:[0, 74071, 168488, 184499, 181082, 219510, 217395, 229719, 155483]},
];
const ALL_POSTS=[
  {lbl:'4',m:3,pillar:'Interview',c:'ทำความสะอาดห้องเครื่องอย่างปลอดภัยด้วย WIBWUB Mind',views:10000,eng:121,ret:23,watch:15.6,er:1.21,url:'https://www.tiktok.com/@wibwubcar/video/7613359372290247957'},
  {lbl:'5',m:3,pillar:'Interview',c:'ตอบกลับ @Natakorn ภายในรถโดนน้ำหอมหยดใส่แล้วเป็นรอยด่าง',views:1950,eng:17,ret:13,watch:10.3,er:0.87,url:'https://www.tiktok.com/@wibwubcar/video/7613758465680592149'},
  {lbl:'9',m:3,pillar:'Awareness',c:'ใครที่ตามหาน้ำยาเคลือบที่เช็ดง่ายมาก ง่ายๆพอๆกับ quick detailer แนะนำ Reflex',views:2821,eng:50,ret:19,watch:18.1,er:1.77,url:'https://www.tiktok.com/@wibwubcar/video/7615082254229835029'},
  {lbl:'13',m:3,pillar:'Awareness',c:'Set นี้ทนอย่าต่ำคือสามเดือน คุ้ม!!',views:2482,eng:43,ret:21,watch:11.1,er:1.73,url:'https://www.tiktok.com/@wibwubcar/video/7616582213836066069'},
  {lbl:'14',m:3,pillar:'Interview',c:'คราบขี้ไคล ขัดด้วยมือสบายๆ',views:2820,eng:53,ret:17,watch:11.5,er:1.88,url:'https://www.tiktok.com/@wibwubcar/video/7617073568416894229'},
  {lbl:'15(1)',m:3,pillar:'Interview',c:'Hard coat ตัวเดียวที่ใช้งานง่าย สามารถทำเองได้เลย',views:1272,eng:29,ret:17,watch:9.3,er:2.28,url:'https://www.tiktok.com/@wibwubcar/video/7617345255922322709'},
  {lbl:'15(2)',m:3,pillar:'Sale',c:'สายทำรถเยอะ ต้องจัดแล้ว sugar ขนาด 5 ลิตร ประหยัดสุด!',views:5873,eng:51,ret:12,watch:10.1,er:0.87,url:'https://www.tiktok.com/@wibwubcar/video/7617463910131567892'},
  {lbl:'16',m:3,pillar:'Awareness',c:'ใช้แล้วรถนุ่ม แนะนำ Reflex เลยครับ',views:3599,eng:59,ret:16,watch:11.0,er:1.64,url:'https://www.tiktok.com/@wibwubcar/video/7617857909828996373'},
  {lbl:'18',m:3,pillar:'Interview',c:'คราบครีม แนะนำน้ำยาและทิชชู่เปียก Refresh เลยครับ',views:1377,eng:21,ret:12,watch:11.8,er:1.53,url:'https://www.tiktok.com/@wibwubcar/video/7618469490346544405'},
  {lbl:'19',m:3,pillar:'Interview',c:'เช็ดทำความสะอาดฝุ่นภายในรถพร้อมเพิ่มความหรูให้รถ',views:807,eng:30,ret:21,watch:14.7,er:3.72,url:'https://www.tiktok.com/@wibwubcar/video/7618979877299080468'},
  {lbl:'21',m:3,pillar:'Sale',c:'ทิชชูเปียกสำหรับเช็ดเก็บฝุ่นภายในรถแบบไม่เงา',views:1775,eng:18,ret:10,watch:11.5,er:1.01,url:'https://www.tiktok.com/@wibwubcar/video/7619679440087387412'},
  {lbl:'23',m:3,pillar:'Knowledge',c:'ไม่ใช่แค่เงา แต่ให้ความนุ่มมือจัดๆเลยตัวนี้',views:2228,eng:14,ret:11,watch:9.1,er:0.63,url:'https://www.tiktok.com/@wibwubcar/video/7620461024252022037'},
  {lbl:'24',m:3,pillar:'Review',c:'ผ้าที่เช็ดรถต้องเป็นผ้าไร้ขอบเท่านั้น ทำยังไงผิวรถจะไม่เกิดรอย',views:674,eng:14,ret:24,watch:21.0,er:2.08,url:'https://www.tiktok.com/@wibwubcar/video/7620696304791997716'},
  {lbl:'27',m:3,pillar:'Interview',c:'กระจกมองข้างไม่ควรใช้น้ำยาขจัดคราบอื่นๆ เพราะมีสารปรอทเคลือบอยู่',views:5025,eng:59,ret:16,watch:10.1,er:1.17,url:'https://www.tiktok.com/@wibwubcar/video/7621774033184460053'},
  {lbl:'28',m:3,pillar:'Interview',c:'ฟิล์มกันรอย ใช้ Reflex ได้เลย น้ำยาจะไม่บดบังความใส',views:775,eng:17,ret:19,watch:11.5,er:2.19,url:'https://www.tiktok.com/@wibwubcar/video/7622146885205101845'},
  {lbl:'29',m:3,pillar:'Interview',c:'น้ำยา 2 ตัวนี้ใช้กับกระจกเหมือนกัน แต่จุดประสงค์ต่างกัน',views:401,eng:16,ret:23,watch:11.7,er:3.99,url:'https://www.tiktok.com/@wibwubcar/video/7622697526558297364'},
  {lbl:'1',m:4,pillar:'Brand Expert',c:'เริ่มแล้วนะค้าบ แจกจนกว่าของจะหมด',views:1162,eng:24,ret:14,watch:16.1,er:2.07,url:'https://www.tiktok.com/@wibwubcar/video/7623632463067204885'},
  {lbl:'2',m:4,pillar:'Interview',c:'คราบน้ำบาดาล มักมีระดับความรุนแรง 2 แบบ',views:1864,eng:24,ret:12,watch:8.4,er:1.29,url:'https://www.tiktok.com/@wibwubcar/video/7624158274631355668'},
  {lbl:'8',m:4,pillar:'Knowledge',c:'วิธีลดฝุ่นภายในรถ ยิ่งโดนเฉพาะไฟฟ้าสถิต ใช้ interior ช่วยได้เยอะ',views:7086,eng:47,ret:19,watch:6.6,er:0.66,url:'https://www.tiktok.com/@wibwubcar/video/7626204813130206485'},
  {lbl:'9(1)',m:4,pillar:'Lifestyle',c:'เพื่อน้องกี้พี่ทำได้',views:678,eng:16,ret:20,watch:5.6,er:2.36,url:'https://www.tiktok.com/@wibwubcar/video/7626743389312290068'},
  {lbl:'9(2)',m:4,pillar:'Lifestyle',c:'เป็นสายไหนกันครับ ส่วนแอดสายตี้',views:1214,eng:28,ret:19,watch:9.2,er:2.31,url:'https://www.tiktok.com/@wibwubcar/video/7626747160221994260'},
  {lbl:'11(1)',m:4,pillar:'Lifestyle',c:'มันมาพร้อมสงกรานต์จ้า',views:811,eng:24,ret:21,watch:7.7,er:2.96,url:'https://www.tiktok.com/@wibwubcar/video/7627271347642666261'},
  {lbl:'11(2)',m:4,pillar:'Review',c:'คราบเล็กๆน้อยๆในรถ น่ารำคาญ กว่าจะรอล้างรถก็เป็นเดือน ใช้ interior',views:1650,eng:16,ret:16,watch:10.3,er:0.97,url:'https://www.tiktok.com/@wibwubcar/video/7627274372343926036'},
  {lbl:'13',m:4,pillar:'Knowledge',c:'รถมีตัวกรองที่ปล่อยประจุออกมาในอากาศ ทำให้ฝุ่นหนักขึ้น',views:1317,eng:14,ret:13,watch:7.0,er:1.06,url:'https://www.tiktok.com/@wibwubcar/video/7628088343728803093'},
  {lbl:'14(1)',m:4,pillar:'Knowledge',c:'3 ตัวนี้ใช้ล้างสี เคลียร์คราบพร้อมเคลือบจบหลังสงกรานต์',views:2570,eng:49,ret:22,watch:10.8,er:1.91,url:'https://www.tiktok.com/@wibwubcar/video/7628320150613413140'},
  {lbl:'14(2)',m:4,pillar:'Knowledge',c:'หลังใช้ตัวนี้แล้วต้องเคลือบซ้ำไหม? จริงๆตัวนี้มีสารเคลือบในตัว',views:1066,eng:11,ret:18,watch:14.5,er:1.03,url:'https://www.tiktok.com/@wibwubcar/video/7628322986457664789'},
  {lbl:'16(1)',m:4,pillar:'Review',c:'ตัวเปียกแล้วนั่งในรถ ซักพักนึงมีกลิ่นอับ สามารถใช้ตัวนี้ได้',views:1142,eng:21,ret:14,watch:12.1,er:1.84,url:'https://www.tiktok.com/@wibwubcar/video/7629375813334453524'},
  {lbl:'16(2)',m:4,pillar:'Knowledge',c:'ใช้น้ำเปล่าเช็ดก็ได้นี่!',views:2346,eng:51,ret:16,watch:11.1,er:2.17,url:'https://www.tiktok.com/@wibwubcar/video/7629378263047097620'},
  {lbl:'20(1)',m:4,pillar:'Review',c:'ตัวสามัญประจำรถ แอดเองยังเอาติดไว้ข้างรถเลย',views:2073,eng:31,ret:14,watch:8.6,er:1.50,url:'https://www.tiktok.com/@wibwubcar/video/7630800267550051605'},
  {lbl:'20(2)',m:4,pillar:'Other',c:'เอาคราบน้ำ คราบแป้งสงกรานต์ที่ล้างยังไงก็ล้างไม่ออก จะออกด้วยวิธีนี้',views:5245,eng:71,ret:19,watch:11.3,er:1.35,url:'https://www.tiktok.com/@wibwubcar/video/7630802122954591509'},
  {lbl:'21',m:4,pillar:'Knowledge',c:'น้ำยาภายในของแบรนด์จะไม่มีกลิ่น เพราะกลิ่นที่เติมลงไปมีสารระเหย',views:1784,eng:34,ret:18,watch:13.3,er:1.91,url:'https://www.tiktok.com/@wibwubcar/video/7631220953447451925'},
  {lbl:'26',m:4,pillar:'Knowledge',c:'เวลาทำความสะอาดรถ จะทำก็ต่อเมื่อเริ่มสกปรกตามความรู้สึก',views:935,eng:7,ret:13,watch:9.0,er:0.75,url:'https://www.tiktok.com/@wibwubcar/video/7633008671806590229'},
  {lbl:'27(1)',m:4,pillar:'Knowledge',c:'สาเหตุที่ WIBWUB ไม่ใส่กลิ่นสำหรับภายในก็เพราะสาเหตุนี้',views:2205,eng:34,ret:15,watch:13.6,er:1.54,url:'https://www.tiktok.com/@wibwubcar/video/7633009672647134485'},
  {lbl:'27(2)',m:4,pillar:'Knowledge',c:'ตัวบรรยากาศสามารถใช้ได้สองวิธี คือฉีดที่พรมหรือฉีดไปยังจุดกำเนิดกลิ่น',views:1161,eng:23,ret:20,watch:11.3,er:1.98,url:'https://www.tiktok.com/@wibwubcar/video/7633402927331298581'},
  {lbl:'29',m:4,pillar:'Knowledge',c:'ไม่ต้องปัดฝุ่นก่อน ตัวนี้ฉีดแล้วเช็ดได้เลย เก็บฝุ่นพร้อมทำความสะอาดในขั้นตอนเดียว',views:2311,eng:25,ret:15,watch:10.8,er:1.08,url:'https://www.tiktok.com/@wibwubcar/video/7634142870022327573'},
  {lbl:'30',m:4,pillar:'Review',c:'ผ้าซับน้ำ Monster ผืนใหญ่ ทั้งคันเอาอยู่จริง',views:1828,eng:26,ret:13,watch:8.8,er:1.42,url:'https://www.tiktok.com/@wibwubcar/video/7634542191947336978'},
  {lbl:'1',m:5,pillar:'Review',c:'ภายนอกใส ภายในเนี๊ยบ 2 ตัวนี้มีติดรถไว้ จบเรื่องฝุ่น ดูแลรถได้ทุกวัน',views:2363,eng:40,ret:16,watch:8.0,er:1.69,url:'https://www.tiktok.com/@wibwubcar/video/7634920106979527954'},
  {lbl:'2',m:5,pillar:'Knowledge',c:'ก็แดดมันร้อน ป้องกันด้วย UV Protect วัสดุภายในไม่ซีด ไม่หมองไว',views:2028,eng:25,ret:13,watch:7.9,er:1.23,url:'https://www.tiktok.com/@wibwubcar/video/7635265940803865874'},
  {lbl:'3',m:5,pillar:'Sale',c:'มีค่า pH-Balance ไม่กัดเบาะ เช็ดได้ทุกพื้นผิวภายในรถ',views:2019,eng:25,ret:12,watch:12.4,er:1.24,url:'https://www.tiktok.com/@wibwubcar/video/7635643444492373266'},
  {lbl:'4',m:5,pillar:'Knowledge',c:'น้ำยาเช็ดเก็บ Mind ดีกว่าครับ ออกแบบมาเพื่อเก็บฝุ่นโดยเฉพาะ',views:4610,eng:55,ret:19,watch:12.6,er:1.19,url:'https://www.tiktok.com/@wibwubcar/video/7636010576790965511'},
  {lbl:'5',m:5,pillar:'Review',c:'ตรวจสอบรถก่อนฝน Interior ดูแลภายในได้หลายอย่างมาก',views:2874,eng:39,ret:14,watch:9.4,er:1.36,url:'https://www.tiktok.com/@wibwubcar/video/7636362979667332360'},
  {lbl:'6',m:5,pillar:'Knowledge',c:'ใครชอบฟีลลิ่งรถใส ๆ ลื่นมือ แนะนำ Reflex ยิ่งเป็นรถสีอ่อนยิ่งเล่นแสงดี',views:3922,eng:49,ret:12,watch:15.4,er:1.25,url:'https://www.tiktok.com/@wibwubcar/video/7636747733226900743'},
  {lbl:'8',m:5,pillar:'Review',c:'ฝนตกแค่ไหน ก็ไม่บดบังทัศนวิสัย',views:4027,eng:74,ret:19,watch:15.4,er:1.84,url:'https://www.tiktok.com/@wibwubcar/video/7637424902663965970'},
  {lbl:'12',m:5,pillar:'Knowledge',c:'ตัวนี้เช็ดภายในได้หมด บอกเลยสบายใจแน่นอน',views:1164,eng:24,ret:15,watch:10.9,er:2.06,url:'https://www.tiktok.com/@wibwubcar/video/7638998231061433607'},
  {lbl:'13(2)',m:5,pillar:'Review',c:'ทำความสะอาดห้องเครื่องใช้ APC Car Cleaner ฉีดแล้วเช็ดออกได้เลย',views:1493,eng:27,ret:20,watch:9.5,er:1.81,url:'https://www.tiktok.com/@wibwubcar/video/7639366337583746311'},
  {lbl:'13(1)',m:5,pillar:'Knowledge',c:'ตอบกลับ @น้องเงินออม Mind ใช้เช็ดเก็บฝุ่นภายนอก Ceramic Quick Detailer',views:1138,eng:19,ret:22,watch:19.7,er:1.67,url:'https://www.tiktok.com/@wibwubcar/video/7639179491033484562'},
  {lbl:'14',m:5,pillar:'Lifestyle',c:'มาดูกันว่าแอดมิน wibwub เป็นสายไหนกัน',views:592,eng:15,ret:18,watch:14.7,er:2.53,url:'https://www.tiktok.com/@wibwubcar/video/7639732629201276167'},
  {lbl:'15',m:5,pillar:'Knowledge',c:'ทำความสะอาดกระจกภายในรถที่ติดฟิล์มกรองแสง',views:952,eng:21,ret:27,watch:18.3,er:2.21,url:'https://www.tiktok.com/@wibwubcar/video/7640111377654435079'},

  {lbl:'18',m:5,pillar:'Knowledge',c:'ผ้าสำหรับรถมีหลายประเภท ให้ดีต้องไร้ขอบ เช็ดรถจะไม่ทำให้รอย',views:1251,eng:47,ret:20,watch:13.0,er:3.76,url:'https://www.tiktok.com/@wibwubcar/video/7641217132268735762'},
  {lbl:'19',m:5,pillar:'Review',c:'เช็ดแล้วได้ผิวสัมผัสแมตต์แบบนี้เลย ฟีลลิ่งเหมือนรถออกใหม่',views:1040,eng:14,ret:13,watch:10.0,er:1.35,url:'https://www.tiktok.com/@wibwubcar/video/7641597742820625672'},
  {lbl:'20',m:5,pillar:'Knowledge',c:'ถ้าอยากลบคราบน้ำแนะนำ spot clean นะครับ',views:1136,eng:28,ret:29,watch:14.4,er:2.46,url:'https://www.tiktok.com/@wibwubcar/video/7641956452105702664'},
  {lbl:'21',m:5,pillar:'Lifestyle',c:'ปิดตาทายกลิ่น มาดูกันว่าแอดมินคนไหนเซียนที่สุด',views:360,eng:17,ret:16,watch:9.3,er:4.72,url:'https://www.tiktok.com/@wibwubcar/video/7642332908249976071'},
  {lbl:'22',m:5,pillar:'Review',c:'ตัวนี้เป็น pH balanced ไม่กัดมือ ปลอดภัยแน่นอนครับ',views:525,eng:3,ret:0,watch:12.0,er:0.57,url:'https://www.tiktok.com/@wibwubcar/video/7642702488696638727'},
  {lbl:'23(1)',m:5,pillar:'Lifestyle',c:'ไล่น้ำเทพๆ ติดทนหลายเดือน เคลือบครั้งเดียว หมดฤดูฝน',views:1124,eng:11,ret:18,watch:5.8,er:0.98,url:'https://www.tiktok.com/@wibwubcar/video/7642947868566867221'},
  {lbl:'23(2)',m:5,pillar:'Lifestyle',c:'Sugar = ฉ่ำ เข้ม ไล่น้ำ',views:1475,eng:18,ret:17,watch:3.6,er:1.22,url:'https://www.tiktok.com/@wibwubcar/video/7643111217829022996'},
  {lbl:'25',m:5,pillar:'Review',c:'หน้าฝนมาแล้วเคลือบกระจกกันครับ ไล่น้ำดีแถมอยู่นานหลายเดือน',views:780,eng:11,ret:25,watch:9.9,er:1.41,url:'https://www.tiktok.com/@wibwubcar/video/7643814294827715848'},
  {lbl:'26(1)',m:5,pillar:'Knowledge',c:'ตัวช่วยเช็ดเก็บฝุ่นภายใน ที่พร้อมเคลือบภายในตัว แล้ววัสดุดูใหม่ luxury gloss',views:1364,eng:14,ret:13,watch:3.8,er:1.03,url:'https://www.tiktok.com/@wibwubcar/video/7644189184596561170'},
  {lbl:'26(2)',m:5,pillar:'Lifestyle',c:'ก็ปกติป้ะครับ',views:10184,eng:204,ret:53,watch:13.2,er:2.00,url:'https://www.tiktok.com/@wibwubcar/video/7644218791974800661'},
  {lbl:'27',m:5,pillar:'Review',c:'ทุเรียนกินได้ครับ แต่กลิ่นไม่ควรอยู่ในรถ BANYAKART ช่วยได้',views:1160,eng:19,ret:20,watch:5.6,er:1.64,url:'https://www.tiktok.com/@wibwubcar/video/7644555338385083656'},
  {lbl:'28',m:5,pillar:'Review',c:'รถใหม่ดูแลตั้งแต่ต้น เบาะรถก็สวยนุ่มไปได้อีกหลายปี',views:502,eng:8,ret:16,watch:6.3,er:1.59,url:'https://www.tiktok.com/@wibwubcar/video/7644871371809361160'},
  {lbl:'29',m:5,pillar:'Lifestyle',c:'[Lifestyle]',views:484,eng:15,love:15,comment:0,share:0,save:0,ret:15.0,watch:6.78,er:3.1,url:'#'},
  {lbl:'1',m:6,pillar:'Sale',c:'ถ้าไม่อยากพลาดโปรเด็ดในไลฟ์ 6.6 นี้เจอกัน',views:751,eng:12,love:11,comment:0,share:1,save:0,ret:13,watch:24.55,er:1.60,url:'https://vt.tiktok.com/ZSQ1SVGgK/'},
  {lbl:'2 (1)',m:6,pillar:'Review',c:'มุมมองหลังเคลือบกระจก ตอนฝนตก วิสัยทัศน์ก็ยังชัด 😎',views:2258,eng:31,love:30,comment:0,share:1,save:0,ret:0,watch:0,er:1.37,url:'https://vt.tiktok.com/ZSQ1SqcPp/'},
  {lbl:'2 (2)',m:6,pillar:'Lifestyle',c:'พฤติกรรม คนรักรถ ที่คนอื่นมองว่าแปลก',views:2128,eng:17,love:15,comment:0,share:1,save:1,ret:19,watch:15.32,er:0.80,url:'https://vt.tiktok.com/ZSQ1AL6Ur/'},
  {lbl:'3',m:6,pillar:'Other',c:'กลิ่นอับ ฝุ่นก็เยอะแค่ไหน สองตัวนี้เอาอยู่ครับ',views:789,eng:14,love:12,comment:0,share:2,save:0,ret:15,watch:8.97,er:1.77,url:'https://vt.tiktok.com/ZSQ1ShcAu/'},
  {lbl:'4',m:6,pillar:'Review',c:'ใช้ง่าย ไม่เสียเหงื่อ แค่ "ฉีด + ฟลัช" ก็เคลือบได้ทั้งคัน',views:3140,eng:41,love:35,comment:3,share:1,save:2,ret:19,watch:19.19,er:1.31,url:'https://www.tiktok.com/@wibwubcar/video/7647503398631230728'},
  {lbl:'5',m:6,pillar:'Lifestyle',c:'3 คำสำหรับรถที่เงาและฉ่ำ',views:3732,eng:47,love:45,comment:0,share:0,save:2,ret:16,watch:18.52,er:1.26,url:'https://www.tiktok.com/@wibwubcar/video/7647894752230247700'},
  {lbl:'8',m:6,pillar:'Review',c:'แห้งแบบไม่ต้องออกแรง superdry series !',views:796,eng:9,love:6,comment:0,share:2,save:1,ret:17,watch:16.96,er:1.13,url:'https://www.tiktok.com/@wibwubcar/video/7648695799605480725'},
  {lbl:'8 (1)',m:6,pillar:'Sale',c:'Reflex เงาใส เล่นแสงวิ้งๆ อยู่ติดทนถึง 3 เดือนครับ',views:4391,eng:59,love:46,comment:0,share:5,save:8,ret:17,watch:12.59,er:1.34,url:'https://www.tiktok.com/@wibwubcar/video/7648934210413006088'},
  {lbl:'9',m:6,pillar:'Lifestyle',c:'เคยสงสัยมั้ย? ทำไมต้องใส่ถุงมือขับรถ',views:1392,eng:28,love:24,comment:2,share:0,save:2,ret:27,watch:16.59,er:2.01,url:'https://www.tiktok.com/@wibwubcar/video/7649375146087681287'},
  {lbl:'10',m:6,pillar:'Review',c:'ในวันที่ปวดหลัง 😅 ก็เคลือบรถง่ายๆ ไม่เสียเหงื่อครับ',views:1959,eng:38,love:33,comment:0,share:2,save:3,ret:24,watch:19.49,er:1.94,url:'https://www.tiktok.com/@wibwubcar/video/7649746680962731272'},
  {lbl:'11',m:6,pillar:'Knowledge',c:'ฝุ่นมาเมื่อไหร่ หยิบใช้ได้เลยครับ 😎🚘',views:763,eng:14,love:11,comment:1,share:2,save:0,ret:21,watch:13.34,er:1.84,url:'https://www.tiktok.com/@wibwubcar/video/7650108703131176199'},
  {lbl:'15',m:6,pillar:'Review',c:'หน้าฝนแบบนี้ต้องเคลือบกระจกด้วยตัวนี้เลยครับ',views:1745,eng:29,love:26,comment:0,share:2,save:1,ret:18,watch:18.36,er:1.66,url:'https://www.tiktok.com/@wibwubcar/video/7651602201663507733'},
  {lbl:'16',m:6,pillar:'Review',c:'คราบมันที่กระจกขวดนี้เอาอยู่ทั้งในและนอกเลยครับ',views:4550,eng:65,love:60,comment:0,share:1,save:4,ret:26,watch:13.50,er:1.43,url:'https://www.tiktok.com/@wibwubcar/video/7651991605959740692'},
  {lbl:'17',m:6,pillar:'Lifestyle',c:'ล้างรถเองจัดเซ็ทนี้เลยครับ',views:1468,eng:26,love:25,comment:0,share:1,save:0,ret:22,watch:15.42,er:1.77,url:'https://www.tiktok.com/@wibwubcar/video/7652370145628785940'},
  {lbl:'18',m:6,pillar:'Knowledge',c:'รีบใช้รถแต่ไม่มีเวลาล้างจัดขวดนี้เลยครับ',views:1023,eng:21,love:18,comment:0,share:2,save:1,ret:20,watch:11.92,er:2.05,url:'https://www.tiktok.com/@wibwubcar/video/7652734740415499541'},
  {lbl:'19',m:6,pillar:'Review',c:'ภายในสะอาดฝุ่นหายรอยนิ้วมือเกลี้ยง',views:695,eng:16,love:13,comment:0,share:2,save:1,ret:14,watch:12.14,er:2.30,url:'https://www.tiktok.com/@wibwubcar/video/7653098122238872852'},
  {lbl:'22',m:6,pillar:'Review',c:'ล้างรถไม่ต้องใช้น้ำ แถมประหยัด WIBWUB Waterless ตัวนี้เลยครับ',views:2424,eng:42,love:37,comment:1,share:0,save:4,ret:18,watch:11.49,er:1.73,url:'https://www.tiktok.com/@wibwubcar/video/7654230248040598802'},
  {lbl:'22 (1)',m:6,pillar:'Review',c:'เคลือบสีทน 1 ปี ทำเองได้ง่ายๆครับ',views:2421,eng:17,love:17,comment:0,share:0,save:0,ret:15,watch:7.25,er:0.70,url:'https://www.tiktok.com/@wibwubcar/video/7654533731117468948'},
  {lbl:'23',m:6,pillar:'Lifestyle',c:'Wheel & Tire Clean ASMR 🔊',views:717,eng:14,love:13,comment:0,share:0,save:1,ret:21,watch:9.69,er:1.95,url:'https://www.tiktok.com/@wibwubcar/video/7654579608284581128'},
  {lbl:'24',m:6,pillar:'Review',c:'ทำความสะอาดเบาะด้วย Refresh กันครับ',views:1552,eng:17,love:14,comment:0,share:1,save:2,ret:15,watch:10.41,er:1.10,url:'https://www.tiktok.com/@wibwubcar/video/7654867216873180423'},
  {lbl:'24 (1)',m:6,pillar:'Review',c:'Sugar น้ำยาเคลือบตัวโปรด รถฉ่ำเหมือนถังหูลู่',views:2167,eng:47,love:18,comment:0,share:27,save:2,ret:12,watch:6.24,er:2.17,url:'https://www.tiktok.com/@wibwubcar/video/7654900657236888850'},
  {lbl:'24 (2)',m:6,pillar:'Review',c:'รถติดฟิมล์ แนะนำตัวนี้ครับ',views:2134,eng:30,love:29,comment:0,share:0,save:1,ret:15,watch:9.26,er:1.41,url:'https://www.tiktok.com/@wibwubcar/video/7654980773233102087'},
  {lbl:'25',m:6,pillar:'Sale',c:'อยู่ยาวๆ เคลือบติดทนนาน 2 ปี',views:1302,eng:19,love:18,comment:0,share:0,save:1,ret:19,watch:13.67,er:1.46,url:'https://www.tiktok.com/@wibwubcar/video/7655150378694003976'},
  {lbl:'25 (1)',m:6,pillar:'Sale',c:'ทิชชู่กลับมาแล้ว Refresh/Interior ภายในสะอาดใช้สะดวก',views:4032,eng:21,love:18,comment:1,share:1,save:1,ret:7,watch:13.31,er:0.52,url:'https://www.tiktok.com/@wibwubcar/video/7655177124118154504'},
  {lbl:'25 (2)',m:6,pillar:'Review',c:'ไล่น้ำเป็น Sheeting เหมาะสำหรับหน้าฝนสุดๆ',views:3175,eng:60,love:52,comment:2,share:2,save:4,ret:29,watch:17.64,er:1.89,url:'https://www.tiktok.com/@wibwubcar/video/7655239869739977991'},
  {lbl:'26',m:6,pillar:'Review',c:'ตอบกลับ @อ.นุ บ้านรัชดา... Sugar เคลือบภายนอกฉ่ำและภายในเคลือบได้ไหม?',views:974,eng:14,love:14,comment:0,share:0,save:0,ret:18,watch:11.86,er:1.44,url:'https://www.tiktok.com/@wibwubcar/video/7655679901047082248'},
  {lbl:'27',m:6,pillar:'Lifestyle',c:'สุ่มเช็ดรถให้พี่วิน มาดูกันอุปกรณ์น้อยจะทำความสะอาดได้ไหม?',views:1156,eng:29,love:29,comment:0,share:0,save:0,ret:18,watch:9.03,er:2.51,url:'https://www.tiktok.com/@wibwubcar/video/7129377558268890394'},
  {lbl:'28',m:6,pillar:'Review',c:'เช็ดเก็บฝุ่นหาย ภายในไม่เหนียว',views:112,eng:3,love:3,comment:0,share:0,save:0,ret:13,watch:6.50,er:2.68,url:'https://www.tiktok.com/@wibwubcar/video/7656413786986794260'},
  {lbl:'29/6/26',m:6,pillar:'Lifestyle',c:'[Lifestyle]',views:5731,eng:125,love:103,comment:0,share:3,save:19,ret:18.0,watch:16.46,er:2.18,url:'#'},
  {lbl:'30/6/26',m:6,pillar:'Review',c:'[Review]',views:2157,eng:36,love:29,comment:0,share:0,save:7,ret:20.0,watch:14.41,er:1.67,url:'#'},
  {lbl:'2/7/26',m:7,pillar:'Sale',c:'[Sale]',views:938,eng:8,love:8,comment:0,share:0,save:0,ret:20.0,watch:14.2,er:0.85,url:'#'},
  {lbl:'4/7/26',m:7,pillar:'Knowledge',c:'[Knowledge]',views:1824,eng:45,love:43,comment:0,share:2,save:0,ret:20.0,watch:9.13,er:2.47,url:'#'},
];

// ════════════════════════════════════════
// UTILS
// ════════════════════════════════════════
const fmtB=v=>v>=1e6?'฿'+(v/1e6).toFixed(1)+'M':v>=1000?'฿'+Math.round(v/1000)+'K':'฿'+v;
const fmtN=v=>v>=1e6?(v/1e6).toFixed(1)+'M':v>=1000?Math.round(v/1000)+'K':''+v;
const pct=(a,b)=>{if(!b)return'—';const p=(a-b)/b*100;return(p>=0?'↑':'↓')+Math.abs(p).toFixed(1)+'%';};
const pctColor=(a,b)=>a>=b?'color:var(--green)':'color:var(--red)';
const rkStyle=i=>i===0?'background:#FEF3C7;color:#92400E':i===1?'background:#F3F4F6;color:#6B7280':i===2?'background:#EEF3FD;color:#1A5CDB':'background:#F9FAFB;color:#9CA3AF';
const pillCls=p=>({Interview:'pi',Knowledge:'pt',Review:'pa',Awareness:'paw',Sale:'pc2',Lifestyle:'pp','Brand Expert':'pp',Other:'po'}[p]||'pp');
const mColor={3:'#2878d0',4:'#c4406e',5:'#1b9664',6:'#9333ea',7:'#ea8c33'};

function bar(val,max,color,label,right){
  const w=max>0?Math.round(val/max*100):0;
  return`<div style="margin-bottom:8px">
    <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px">
      <span style="font-weight:600">${label}</span><span style="color:var(--bl);font-weight:700">${right||fmtB(val)}</span>
    </div>
    <div class="bar-bg"><div class="bar-fill" style="width:${w}%;background:${color}"></div></div>
  </div>`;
}

// ════════════════════════════════════════
// NAV
// ════════════════════════════════════════
function nav(p){
  const role=window._userRole||'';
  const allowed={
    admin:         ['home','sales','mk','attendance','hr','procurement','admin'],
    head_marketing:['home','sales','mk','attendance','procurement'],
    kol_team:      ['mk','attendance'],
    content_team:  ['mk','attendance'],
    hr_team:       ['attendance'],
    procurement:   ['procurement','attendance'],
  }[role]||['home','sales','mk','attendance'];
  if(!allowed.includes(p))return;
  document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));
  document.querySelectorAll('.ni').forEach(x=>x.classList.remove('active'));
  document.getElementById('pg-'+p).classList.add('active');
  const navEl=document.getElementById('nav-'+p);
  if(navEl)navEl.classList.add('active');
  document.getElementById('mainScreen').scrollTop=0;
  if(p==='admin') loadAdminUsers();
  if(p==='attendance') initHR();
  if(p==='hr') initHRDash();
}
function sTab(i,el){switchSv('s',i,el,'sales-tabs');}
function mTab(i,el){switchSv('m',i,el,'mk-tabs');}
function switchSv(pfx,i,el,tabsId){
  document.querySelectorAll('#'+tabsId+' .stab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('[id^="'+pfx+'-sv-"]').forEach(v=>v.classList.remove('active'));
  el.classList.add('active');
  document.getElementById(pfx+'-sv-'+i).classList.add('active');
  document.getElementById('mainScreen').scrollTop=0;
}

// ════════════════════════════════════════
// DERIVED LABELS / MONTH TABS
// สร้าง tab เดือนจาก M5 โดยตรง เพื่อไม่ให้ tab ค้างอยู่ที่เดือนเก่าหลัง sync
// (เคยค้างที่ พ.ค. ทั้งที่ข้อมูลถึง ส.ค. แล้ว)
// ════════════════════════════════════════
function buildMoTabs(){
  const last=M5.length-1;
  [['s-mo-tabs','setSMo'],['s-plt-tabs','setSPlt'],['ads-mo-tabs','setAdsMo']].forEach(([id,fn])=>{
    const c=document.getElementById(id); if(!c) return;
    c.innerHTML=M5.map((m,i)=>`<div class="mtab${i===0?' active':''}" onclick="${fn}(${i},this)">${m}${i===last?'*':''}</div>`).join('');
  });
  document.querySelectorAll('.rng-lbl').forEach(n=>{ n.textContent=salesRangeTH(); });
  document.querySelectorAll('.pmo-note').forEach(n=>{ n.textContent=salesPartialNote(); });
  const h=document.getElementById('mob-hdr-right'); if(h) h.setAttribute('data-updated',salesAsofTH());
}

// ════════════════════════════════════════
// HOME
// ════════════════════════════════════════
function initHome(){
  buildMoTabs();
  // ยอดสะสมต่อ platform บน hero — คำนวณจาก array จริง ไม่ hardcode (กันค่าค้างหลัง sync)
  const _sum=a=>a.reduce((s,v)=>s+v,0);
  const _setM=(id,v)=>{const e=document.getElementById(id); if(e) e.textContent='฿'+(v/1e6).toFixed(v/1e6>=10?1:2)+'M';};
  _setM('hhg-sh',_sum(SH_REV)); _setM('hhg-tk',_sum(TK_REV)); _setM('hhg-lz',_sum(LZ_REV));
  const _tr=_sum(TOTAL_REV), _to=_sum(TOTAL_ORD);
  const _t=(id,v)=>{const e=document.getElementById(id); if(e) e.textContent=v;};
  _t('hh-lbl',`ยอดขายรวม ${salesRangeTH()}`);
  _t('hh-val','฿'+(_tr/1e6).toFixed(1)+'M');
  _t('hh-sub',`${_to.toLocaleString()} unique orders · AOV ฿${Math.round(_tr/_to).toLocaleString()}`);
  const tot=CHANNELS.reduce((s,c)=>s+c.v,0);
  const maxV=CHANNELS[0].v;
  document.getElementById('home-ch').innerHTML=CHANNELS.map(c=>`
    <div style="margin-bottom:8px">
      <div class="ch-row"><div class="ch-dot" style="background:${c.color}"></div><div class="ch-name">${c.n}</div><div class="ch-val">${fmtB(c.v)}</div></div>
      <div class="bar-bg"><div class="bar-fill" style="width:${Math.round(c.v/maxV*100)}%;background:${c.color}"></div></div>
      <div class="ch-pct">${(c.v/tot*100).toFixed(1)}% ของยอดรวม</div>
    </div>`).join('');
  document.getElementById('home-prods').innerHTML=ALL_PRODUCTS.slice(0,3).map((p,i)=>`
    <div class="prod-row">
      <div class="prk prk${i<3?i+1:'n'}">${i+1}</div>
      <div class="prod-name">${p.n}</div>
      <div class="prod-right"><div class="prod-val">${fmtB(p.v)}</div><div class="prod-q">${p.q.toLocaleString()} pcs</div></div>
    </div>`).join('');
}

// ════════════════════════════════════════
// SALES OVERVIEW
// ════════════════════════════════════════
let sMo=0;
function initSalesOv(){
  const _tr=TOTAL_REV.reduce((s,v)=>s+v,0), _to=TOTAL_ORD.reduce((s,v)=>s+v,0);
  document.getElementById('s-ov-kpi').innerHTML=`
    <div class="kc"><div class="kc-lbl">ยอดขายรวม (ม.ค.–${M5[M5.length-1]})</div><div class="kc-val">฿${(_tr/1e6).toFixed(1)}M</div><div class="kc-sub">ทุก Platform</div></div>
    <div class="kc"><div class="kc-lbl">ออเดอร์รวม</div><div class="kc-val">${_to.toLocaleString()}</div><div class="kc-sub">unique orders</div></div>
    <div class="kc"><div class="kc-lbl">AOV เฉลี่ย</div><div class="kc-val">฿${Math.round(_tr/_to).toLocaleString()}</div><div class="kc-sub">ต่อออเดอร์</div></div>
    <div class="kc"><div class="kc-lbl">ยอดขายเดือนล่าสุด</div><div class="kc-val">${fmtB(TOTAL_REV[TOTAL_REV.length-1])}</div><div class="kc-sub">${M5[M5.length-1]} (ถึง ${salesAsofTH()})</div></div>`;
  buildMoTabs();
  setSMo(0,document.querySelector('#s-mo-tabs .mtab'));
  // Rev bars
  const maxR=Math.max(...TOTAL_REV);
  document.getElementById('s-rev-bars').innerHTML=M5.map((m,i)=>`
    <div style="margin-bottom:8px">
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px">
        <span style="font-weight:600">${m}${i===M5.length-1?' *':''}</span><span style="font-weight:700;color:var(--bl)">${fmtB(TOTAL_REV[i])}</span>
      </div>
      <div class="bar-bg" style="height:8px"><div class="bar-fill" style="width:${Math.round(TOTAL_REV[i]/maxR*100)}%;background:${i===M5.length-1?'var(--green)':'var(--bl)'}"></div></div>
      <div style="font-size:10px;color:var(--muted);margin-top:2px">SH ${fmtB(SH_REV[i])} · TK ${fmtB(TK_REV[i])} · LZ ${fmtB(LZ_REV[i])}</div>
    </div>`).join('');
  // Ord bars
  const maxO=Math.max(...M5.map((_,i)=>SH_ORD[i]+TK_ORD[i]+LZ_ORD[i]+FB_ORD[i]+LINE_ORD[i]));
  document.getElementById('s-ord-bars').innerHTML=M5.map((m,i)=>{
    const tot=SH_ORD[i]+TK_ORD[i]+LZ_ORD[i]+FB_ORD[i]+LINE_ORD[i];
    return`<div style="margin-bottom:8px">
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px">
        <span>${m}${i===M5.length-1?' *':''}</span><span style="font-weight:700">${tot.toLocaleString()} orders</span>
      </div>
      <div style="height:8px;background:#f0f0f0;border-radius:4px;overflow:hidden;display:flex">
        <div style="width:${Math.round(SH_ORD[i]/maxO*100)}%;background:var(--sh)"></div>
        <div style="width:${Math.round(TK_ORD[i]/maxO*100)}%;background:#555"></div>
        <div style="width:${Math.round(LZ_ORD[i]/maxO*100)}%;background:var(--lz)"></div>
      </div>
      <div style="font-size:10px;color:var(--muted);margin-top:2px">
        <span style="color:var(--sh)">SH ${SH_ORD[i].toLocaleString()}</span> · TK ${TK_ORD[i].toLocaleString()} · <span style="color:var(--lz)">LZ ${LZ_ORD[i]}</span>
      </div>
    </div>`;}).join('');
}

function setSMo(idx,el){
  sMo=idx;
  document.querySelectorAll('#s-mo-tabs .mtab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  const prev=idx>0?TOTAL_REV[idx-1]:null;
  const mo=prev?`<span style="${pctColor(TOTAL_REV[idx],prev)}">${pct(TOTAL_REV[idx],prev)}</span>`:'—';
  document.getElementById('s-mo-kpi').innerHTML=`
    <div class="kc" style="padding:9px"><div class="kc-lbl">ยอดรวม ${M5[idx]}</div><div class="kc-val" style="font-size:14px">${fmtB(TOTAL_REV[idx])}</div><div class="kc-sub">MoM ${mo}</div></div>
    <div class="kc" style="padding:9px"><div class="kc-lbl">Shopee</div><div class="kc-val" style="font-size:14px;color:var(--sh)">${fmtB(SH_REV[idx])}</div><div class="kc-sub">${SH_ORD[idx].toLocaleString()} orders</div></div>
    <div class="kc" style="padding:9px"><div class="kc-lbl">TikTok</div><div class="kc-val" style="font-size:14px">${fmtB(TK_REV[idx])}</div><div class="kc-sub">${TK_ORD[idx].toLocaleString()} orders</div></div>`;
  renderPlt(idx);
}

// ════════════════════════════════════════
// SALES PLATFORM
// ════════════════════════════════════════
let pltMo=0;
function setSPlt(idx,el){
  pltMo=idx;
  document.querySelectorAll('#s-plt-tabs .mtab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  renderPlt(idx);
}
function renderPlt(idx){
  const el=document.getElementById('s-plt-list');
  if(!el)return;
  const maxR=Math.max(SH_REV[idx],TK_REV[idx],LZ_REV[idx]);
  const shR=(SH_REV[idx]/SH_ADS[idx]).toFixed(2);
  const tkR=(TK_REV[idx]/TK_ADSSPEND[idx]).toFixed(2);
  el.innerHTML=`
  <div class="plt-row">
    <div class="plt-top"><div class="plt-name"><div class="plt-dot" style="background:var(--sh)"></div>Shopee</div><div class="plt-val" style="color:var(--sh)">${fmtB(SH_REV[idx])}</div></div>
    <div class="bar-bg"><div class="bar-fill" style="width:${Math.round(SH_REV[idx]/maxR*100)}%;background:var(--sh)"></div></div>
    <div class="bar-sub">${SH_ORD[idx].toLocaleString()} orders · ยกเลิก ${SH_CANCEL[idx]}%</div>
    <div style="display:flex;gap:12px;margin-top:6px;font-size:11px">
      <span>Ads: <b>${fmtB(SH_ADS[idx])}</b></span>
      <span>ROAS: <b style="color:var(--sh)">${shR}×</b></span>
      <span>Fee: <b>${fmtB(SH_FEE[idx])}</b></span>
    </div>
  </div>
  <div class="plt-row">
    <div class="plt-top"><div class="plt-name"><div class="plt-dot" style="background:#333"></div>TikTok Shop</div><div class="plt-val">${fmtB(TK_REV[idx])}</div></div>
    <div class="bar-bg"><div class="bar-fill" style="width:${Math.round(TK_REV[idx]/maxR*100)}%;background:#333"></div></div>
    <div class="bar-sub">${TK_ORD[idx].toLocaleString()} orders · ยกเลิก ${TK_CANCEL[idx]}%</div>
    <div style="display:flex;gap:12px;margin-top:6px;font-size:11px">
      <span>Affiliate: <b>${fmtB(TK_AFI[idx])}</b></span>
      <span>ROAS: <b>${tkR}×</b></span>
      <span>NET: <b>${fmtB(TK_NET[idx])}</b></span>
    </div>
  </div>
  <div class="plt-row">
    <div class="plt-top"><div class="plt-name"><div class="plt-dot" style="background:var(--lz)"></div>Lazada</div><div class="plt-val" style="color:var(--lz)">${fmtB(LZ_REV[idx])}</div></div>
    <div class="bar-bg"><div class="bar-fill" style="width:${Math.round(LZ_REV[idx]/maxR*100)}%;background:var(--lz)"></div></div>
    <div class="bar-sub">${LZ_ORD[idx]} orders · ยกเลิก ${LZ_CANCEL[idx]}%</div>
    <div style="display:flex;gap:12px;margin-top:6px;font-size:11px">
      <span>Cost%: <b>${LZ_COST_PCT[idx]}%</b></span>
      <span>Ads: <b>${fmtB(LZ_ADS[idx])}</b></span>
    </div>
  </div>
  <div style="margin-top:14px;padding:10px 12px;background:#fef3c7;border:1.5px solid #f59e0b;border-radius:10px;">
    <div style="font-size:10px;font-weight:800;color:#78350f;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px;">⚠️ ยอดที่ไม่ใช่รายได้ (Internal) — Shipnity</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:11px;">
      <div>🔧 Carcare<br><b>${fmtB(CARE_REV[idx])}</b></div>
      <div>📦 เบิกของ<br><b>${fmtB(BEUK_REV[idx])}</b></div>
      <div>🎁 สินค้าทำการตลาด<br><b>${fmtB(MKT_REV[idx])}</b></div>
      <div>🏪 POS หน้าร้าน<br><b>${fmtB(POS_REV[idx])}</b></div>
    </div>
    <div style="margin-top:8px;padding-top:6px;border-top:1px solid #f59e0b;display:flex;justify-content:space-between;font-size:12px;">
      <span style="font-weight:700;color:#78350f;">รวม Internal</span>
      <span style="font-weight:900;color:#d97706;">${fmtB(CARE_REV[idx]+BEUK_REV[idx]+MKT_REV[idx]+POS_REV[idx])}</span>
    </div>
    <div style="font-size:9px;color:#b45309;margin-top:3px;">ไม่นับในยอดรายได้หลัก</div>
  </div>`;
}

// ════════════════════════════════════════
// PRODUCTS
// ════════════════════════════════════════
let prodShown=7,prodMoIdx=-1;
const PROD_MO_LBL=['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค. (1-31)','ก.ย. (1-18)'];
function setProdMo(idx,el){
  prodMoIdx=idx;prodShown=7;
  document.querySelectorAll('#prod-mo-tabs .mtab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  renderProds();
}
function renderProds(){
  const rkCls=i=>i===0?'prk1':i===1?'prk2':i===2?'prk3':'prkn';
  if(prodMoIdx===-1){
    document.getElementById('prod-title').textContent='Top สินค้าขายดี';
    document.getElementById('prod-sub').textContent='ม.ค.–ก.ย. รวม';
    document.getElementById('prod-list').innerHTML=ALL_PRODUCTS.slice(0,prodShown).map((p,i)=>`
      <div class="prod-row" style="flex-wrap:wrap;align-items:flex-start">
        <div class="prk ${rkCls(i)}" style="margin-top:2px">${i+1}</div>
        <div style="flex:1;min-width:0">
          <div class="prod-name">${p.n}</div>
          ${p.mk?`<div style="font-size:10px;color:var(--muted);margin-top:2px">🎯 งบตลาด ${fmtB(p.mk)} · ${p.mkq} ชิ้น</div>`:''}
        </div>
        <div class="prod-right"><div class="prod-val">${fmtB(p.v)}</div><div class="prod-q">${p.q.toLocaleString()} pcs</div></div>
      </div>`).join('');
    document.getElementById('prod-more').style.display=prodShown>=ALL_PRODUCTS.length?'none':'block';
  } else {
    const lbl=PROD_MO_LBL[prodMoIdx];
    document.getElementById('prod-title').textContent='Top สินค้า '+lbl;
    document.getElementById('prod-sub').textContent='ยอดขาย '+lbl+' 2569';
    const hasMoData=PROD_MO[0].mo[prodMoIdx]!==null;
    if(!hasMoData){
      document.getElementById('prod-list').innerHTML=`<div class="inote">ยังไม่มีข้อมูลสินค้ารายเดือนสำหรับ ${lbl} — ดูได้ใน Web Dashboard</div>`;
      document.getElementById('prod-more').style.display='none';
    } else {
      const sorted=[...PROD_MO].filter(p=>p.mo[prodMoIdx]!=null).sort((a,b)=>b.mo[prodMoIdx]-a.mo[prodMoIdx]);
      const maxV=sorted[0].mo[prodMoIdx];
      document.getElementById('prod-list').innerHTML=sorted.map((p,i)=>`
        <div class="prod-row">
          <div class="prk ${rkCls(i)}">${i+1}</div>
          <div style="flex:1">
            <div class="prod-name">${p.n}</div>
            <div class="bar-bg" style="margin-top:3px;height:4px"><div class="bar-fill" style="width:${Math.round(p.mo[prodMoIdx]/maxV*100)}%;background:var(--bl)"></div></div>
          </div>
          <div class="prod-right"><div class="prod-val">${fmtB(p.mo[prodMoIdx])}</div></div>
        </div>`).join('');
      document.getElementById('prod-more').style.display='none';
    }
  }
}
function showMoreProds(){prodShown=ALL_PRODUCTS.length;renderProds();}

// ════════════════════════════════════════
// MONTHLY TABLES
// ════════════════════════════════════════
function initMoTables(){
  document.getElementById('mo-tb-ov').innerHTML=M5.map((m,i)=>{
    const rev=SH_REV[i]+TK_REV[i]+LZ_REV[i];
    const ord=SH_ORD[i]+TK_ORD[i]+LZ_ORD[i];
    const aov=Math.round(rev/ord);
    const prev=i>0?(SH_REV[i-1]+TK_REV[i-1]+LZ_REV[i-1]):null;
    const mo=prev?`<span style="${pctColor(rev,prev)}">${pct(rev,prev)}</span>`:'—';
    return`<tr${i===M5.length-1?' class="hl"':''}><td>${m}${i===M5.length-1?' *':''}</td><td>${fmtB(rev)}</td><td>${ord.toLocaleString()}</td><td>฿${aov.toLocaleString()}</td><td>${mo}</td></tr>`;
  }).join('');
  document.getElementById('mo-tb-sh').innerHTML=M5.map((m,i)=>
    `<tr${i===M5.length-1?' class="hl"':''}><td>${m}</td><td>${fmtB(SH_REV[i])}</td><td>${SH_ORD[i].toLocaleString()}</td><td>${SH_CANCEL[i]}%</td><td>${fmtB(SH_ADS[i])}</td><td style="color:var(--sh)">${(SH_REV[i]/SH_ADS[i]).toFixed(2)}×</td></tr>`
  ).join('');
  document.getElementById('mo-tb-tk').innerHTML=M5.map((m,i)=>
    `<tr${i===M5.length-1?' class="hl"':''}><td>${m}</td><td>${fmtB(TK_REV[i])}</td><td>${TK_ORD[i].toLocaleString()}</td><td>${fmtB(TK_AFI[i])}</td><td>${fmtB(TK_ADSSPEND[i])}</td><td>${(TK_REV[i]/TK_ADSSPEND[i]).toFixed(2)}×</td></tr>`
  ).join('');
  document.getElementById('mo-tb-lz').innerHTML=M5.map((m,i)=>
    `<tr${i===M5.length-1?' class="hl"':''}><td>${m}</td><td>${fmtB(LZ_REV[i])}</td><td>${LZ_ORD[i]}</td><td>${LZ_CANCEL[i]}%</td><td>${LZ_COST_PCT[i]}%</td></tr>`
  ).join('');
}

// ════════════════════════════════════════
// MK OVERVIEW
// ════════════════════════════════════════
function initMkOv(){
  const tg=AFI_GMV.reduce((a,b)=>a+b,0);
  const tn=AFI_NET.reduce((a,b)=>a+b,0);
  const shSpendTot=SH_ADS.reduce((a,b)=>a+b,0);
  const shRevTot=SH_REV.reduce((a,b)=>a+b,0);
  const tkSpendTot=TK_ADSSPEND.reduce((a,b)=>a+b,0);
  const tkRevTot=TK_REV.reduce((a,b)=>a+b,0);
  const shROAS=(shRevTot/shSpendTot).toFixed(2);
  const tkROAS=(tkRevTot/tkSpendTot).toFixed(2);
  document.getElementById('mk-ov-kpi').innerHTML=`
    <div class="kc"><div class="kc-lbl">Affiliate GMV รวม</div><div class="kc-val">${fmtB(tg)}</div><div class="kc-sub">${CREATORS.length} creators · 8 เดือน</div></div>
    <div class="kc"><div class="kc-lbl">Affiliate NET รวม</div><div class="kc-val">${fmtB(tn)}</div><div class="kc-sub">หลังหักค่าคอม</div></div>
    <div class="kc"><div class="kc-lbl">Shopee ROAS เฉลี่ย</div><div class="kc-val" style="color:var(--sh)">${shROAS}×</div><div class="kc-sub">ม.ค.–พ.ค.</div></div>
    <div class="kc"><div class="kc-lbl">TikTok ROAS เฉลี่ย</div><div class="kc-val">${tkROAS}×</div><div class="kc-sub">ม.ค.–พ.ค.</div></div>`;
  const maxG=Math.max(...AFI_GMV);
  document.getElementById('afi-bars').innerHTML=AFI_MONTHS.map((m,i)=>`
    <div style="margin-bottom:7px">
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px">
        <span>${m}</span><span><b style="color:var(--bl)">${fmtB(AFI_GMV[i])}</b> <span style="font-size:10px;color:var(--muted)">NET ${fmtB(AFI_NET[i])}</span></span>
      </div>
      <div class="bar-bg"><div class="bar-fill" style="width:${Math.round(AFI_GMV[i]/maxG*100)}%;background:var(--bl)"></div></div>
    </div>`).join('');
  const shR=SH_REV.map((v,i)=>+(v/SH_ADS[i]).toFixed(2));
  const tkR=TK_REV.map((v,i)=>+(v/TK_ADSSPEND[i]).toFixed(2));
  const maxR=Math.max(...shR,...tkR);
  document.getElementById('roas-bars').innerHTML=M5.map((m,i)=>`
    <div style="margin-bottom:8px">
      <div style="font-size:11px;font-weight:600;margin-bottom:3px">${m}</div>
      <div style="display:flex;gap:5px;align-items:center;margin-bottom:3px">
        <span style="font-size:10px;color:var(--sh);width:28px">SH</span>
        <div class="bar-bg" style="flex:1;margin:0"><div class="bar-fill" style="width:${Math.round(shR[i]/maxR*100)}%;background:var(--sh)"></div></div>
        <span style="font-size:11px;font-weight:700;color:var(--sh);width:34px;text-align:right">${shR[i]}×</span>
      </div>
      <div style="display:flex;gap:5px;align-items:center">
        <span style="font-size:10px;width:28px">TK</span>
        <div class="bar-bg" style="flex:1;margin:0"><div class="bar-fill" style="width:${Math.round(tkR[i]/maxR*100)}%;background:#555"></div></div>
        <span style="font-size:11px;font-weight:700;width:34px;text-align:right">${tkR[i]}×</span>
      </div>
    </div>`).join('');
}

// ════════════════════════════════════════
// AFFILIATE
// ════════════════════════════════════════
let afiKey=6,crShown=15,crSorted=[];
function setAfi(idx,el){
  afiKey=idx;crShown=15;
  document.querySelectorAll('#afi-mo-tabs .mtab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  renderAfi();
}
function renderAfi(){
  crSorted=afiKey==='t'
    ?[...CREATORS].sort((a,b)=>b.t-a.t)
    :[...CREATORS].filter(c=>c.mn[afiKey]!=null).sort((a,b)=>(b.mn[afiKey]??-1)-(a.mn[afiKey]??-1));
  const lbl=afiKey==='t'?'ทั้งหมด':AFI_MONTHS[afiKey];
  if(afiKey==='t'){
    const tg=AFI_GMV.reduce((a,b)=>a+b,0),tn=AFI_NET.reduce((a,b)=>a+b,0);
    document.getElementById('afi-kpi').innerHTML=`
      <div class="kc"><div class="kc-lbl">GMV รวม 8 เดือน</div><div class="kc-val">${fmtB(tg)}</div><div class="kc-sub">${CREATORS.length} creators</div></div>
      <div class="kc"><div class="kc-lbl">NET รวม 7 เดือน</div><div class="kc-val">${fmtB(tn)}</div><div class="kc-sub">หลังหักค่าคอม</div></div>`;
  } else {
    document.getElementById('afi-kpi').innerHTML=`
      <div class="kc"><div class="kc-lbl">GMV ${lbl}</div><div class="kc-val">${fmtB(AFI_GMV[afiKey])}</div><div class="kc-sub">creators ทั้งหมด</div></div>
      <div class="kc"><div class="kc-lbl">NET ${lbl}</div><div class="kc-val">${fmtB(AFI_NET[afiKey])}</div><div class="kc-sub">ค่าคอม ${fmtB(AFI_COMM[afiKey])}</div></div>`;
  }
  const list=crSorted.slice(0,crShown);
  const maxV=list.length>0?(afiKey==='t'?list[0].t:list[0].mn[afiKey]??0):1;
  document.getElementById('cr-list').innerHTML=list.map((c,i)=>{
    const val=afiKey==='t'?c.t:(c.mn[afiKey]??0);
    return`<div class="cr-card">
      <div class="cr-top">
        <div class="cr-rk" style="${rkStyle(i)}">${i+1}</div>
        <div style="flex:1"><div class="cr-name">${c.n}</div><div class="cr-mo">${c.ma}/7 เดือน</div></div>
        <div class="cr-total">${fmtB(val)}</div>
      </div>
      <div class="cr-bar-bg"><div class="cr-bar" style="width:${maxV>0?Math.round(val/maxV*100):0}%"></div></div>
    </div>`;}).join('');
  document.getElementById('cr-more').style.display=crShown>=crSorted.length?'none':'block';
}
function showMoreCr(){crShown+=20;renderAfi();}

// ════════════════════════════════════════
// AFFILIATE VIEW SWITCHER + RECOMMENDATION
// ════════════════════════════════════════
// ════════════════════════════════════════
// ADS
// ════════════════════════════════════════
function switchAds(p){
  ['sh','tk','cb'].forEach(x=>{
    document.getElementById('ap-'+x).className='ap';
    document.getElementById('ads-'+x).classList.remove('active');
  });
  document.getElementById('ap-'+p).className='ap a-'+p;
  document.getElementById('ads-'+p).classList.add('active');
}
let adsMo=0;
function setAdsMo(idx,el){
  adsMo=idx;
  document.querySelectorAll('#ads-mo-tabs .mtab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  renderAdsMo();
}
function renderAdsMo(){
  const i=adsMo;
  const m=M5[i];
  const shR=(SH_REV[i]/SH_ADS[i]).toFixed(2);
  const tkR=(TK_REV[i]/TK_ADSSPEND[i]).toFixed(2);
  const cbR=+((SH_REV[i]+TK_REV[i])/(SH_ADS[i]+TK_ADSSPEND[i])).toFixed(2);
  const shMoM=i>0?`<span style="font-size:10px;${pctColor(SH_REV[i],SH_REV[i-1])}">${pct(SH_REV[i],SH_REV[i-1])}</span>`:'—';
  const tkMoM=i>0?`<span style="font-size:10px;${pctColor(TK_REV[i],TK_REV[i-1])}">${pct(TK_REV[i],TK_REV[i-1])}</span>`:'—';
  document.getElementById('ads-mo-detail').innerHTML=`
    <div style="background:#fff;border-radius:14px;padding:14px;margin-bottom:10px;box-shadow:0 1px 4px rgba(0,0,0,.06)">
      <div style="font-size:12px;font-weight:700;color:var(--muted);margin-bottom:10px;text-transform:uppercase;letter-spacing:.5px">${m}${i===M5.length-1?' *':''} — Ads Detail</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
        <div style="background:#fff4f2;border-radius:10px;padding:10px;border-left:3px solid var(--sh)">
          <div style="font-size:10px;font-weight:700;color:var(--sh);margin-bottom:6px">🧡 SHOPEE</div>
          <div style="font-size:11px;color:var(--muted)">Spend <b style="color:var(--txt)">${fmtB(SH_ADS[i])}</b></div>
          <div style="font-size:11px;color:var(--muted)">Revenue <b style="color:var(--txt)">${fmtB(SH_REV[i])}</b> ${shMoM}</div>
          <div style="font-size:14px;font-weight:800;color:var(--sh);margin-top:5px">${shR}× ROAS</div>
          <div style="font-size:10px;color:var(--muted)">Fee ${fmtB(SH_FEE[i])}</div>
        </div>
        <div style="background:#f5f5f5;border-radius:10px;padding:10px;border-left:3px solid #333">
          <div style="font-size:10px;font-weight:700;color:#333;margin-bottom:6px">🎵 TIKTOK</div>
          <div style="font-size:11px;color:var(--muted)">Spend <b style="color:var(--txt)">${fmtB(TK_ADSSPEND[i])}</b></div>
          <div style="font-size:11px;color:var(--muted)">Revenue <b style="color:var(--txt)">${fmtB(TK_REV[i])}</b> ${tkMoM}</div>
          <div style="font-size:14px;font-weight:800;color:#333;margin-top:5px">${tkR}× ROAS</div>
          <div style="font-size:10px;color:var(--muted)">Fee+Comm ${fmtB(TK_FEECOMM[i])}</div>
        </div>
      </div>
      <div style="margin-top:10px;background:#EEF3FD;border-radius:8px;padding:8px 12px;display:flex;justify-content:space-between;align-items:center">
        <span style="font-size:11px;color:var(--muted)">Combined ROAS</span>
        <span style="font-size:15px;font-weight:800;color:var(--bl)">${cbR}×</span>
        <span style="font-size:11px;color:var(--muted)">Spend รวม ${fmtB(SH_ADS[i]+TK_ADSSPEND[i])}</span>
      </div>
    </div>`;
}
function initAds(){
  renderAdsMo();
  const shSpend=SH_ADS.reduce((a,b)=>a+b,0);
  const shRevT=SH_REV.reduce((a,b)=>a+b,0);
  const tkSpend=TK_ADSSPEND.reduce((a,b)=>a+b,0);
  const tkRevT=TK_REV.reduce((a,b)=>a+b,0);
  const cbSpend=shSpend+tkSpend;
  const cbRevT=shRevT+tkRevT;
  document.getElementById('ads-sh-kpi').innerHTML=`
    <div class="kc"><div class="kc-lbl">Spend รวม</div><div class="kc-val" style="color:var(--sh)">${fmtB(shSpend)}</div><div class="kc-sub">ม.ค.–พ.ค.</div></div>
    <div class="kc"><div class="kc-lbl">ROAS เฉลี่ย</div><div class="kc-val" style="color:var(--sh)">${(shRevT/shSpend).toFixed(2)}×</div><div class="kc-sub">Rev/Spend</div></div>`;
  document.getElementById('ads-tk-kpi').innerHTML=`
    <div class="kc"><div class="kc-lbl">Spend รวม</div><div class="kc-val">${fmtB(tkSpend)}</div><div class="kc-sub">ม.ค.–พ.ค.</div></div>
    <div class="kc"><div class="kc-lbl">ROAS เฉลี่ย</div><div class="kc-val">${(tkRevT/tkSpend).toFixed(2)}×</div><div class="kc-sub">Rev/Spend</div></div>`;
  document.getElementById('ads-cb-kpi').innerHTML=`
    <div class="kc" style="padding:9px"><div class="kc-lbl">Spend รวม</div><div class="kc-val" style="font-size:14px">${fmtB(cbSpend)}</div><div class="kc-sub">SH+TK</div></div>
    <div class="kc" style="padding:9px"><div class="kc-lbl">Revenue</div><div class="kc-val" style="font-size:14px">${fmtB(cbRevT)}</div><div class="kc-sub">SH+TK</div></div>
    <div class="kc" style="padding:9px"><div class="kc-lbl">ROAS รวม</div><div class="kc-val" style="font-size:14px;color:var(--bl)">${(cbRevT/cbSpend).toFixed(2)}×</div><div class="kc-sub">Combined</div></div>`;
  const shR=SH_REV.map((v,i)=>+(v/SH_ADS[i]).toFixed(2));
  const tkR=TK_REV.map((v,i)=>+(v/TK_ADSSPEND[i]).toFixed(2));
  const maxSh=Math.max(...shR),maxTk=Math.max(...tkR);
  document.getElementById('sh-roas-bars').innerHTML=M5.map((m,i)=>`
    <div style="margin-bottom:7px">
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px">
        <span>${m}</span><span style="font-weight:700;color:var(--sh)">${shR[i]}×</span>
      </div>
      <div class="bar-bg"><div class="bar-fill" style="width:${Math.round(shR[i]/maxSh*100)}%;background:var(--sh)"></div></div>
      <div style="font-size:10px;color:var(--muted);margin-top:1px">Spend ${fmtB(SH_ADS[i])} → Rev ${fmtB(SH_REV[i])}</div>
    </div>`).join('');
  document.getElementById('sh-ads-tb').innerHTML=M5.map((m,i)=>
    `<tr${i===M5.length-1?' class="hl"':''}><td>${m}</td><td>${fmtB(SH_ADS[i])}</td><td>${fmtB(SH_FEE[i])}</td><td style="color:var(--sh)">${shR[i]}×</td></tr>`
  ).join('');
  document.getElementById('tk-roas-bars').innerHTML=M5.map((m,i)=>`
    <div style="margin-bottom:7px">
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px">
        <span>${m}</span><span style="font-weight:700">${tkR[i]}×</span>
      </div>
      <div class="bar-bg"><div class="bar-fill" style="width:${Math.round(tkR[i]/maxTk*100)}%;background:#555"></div></div>
      <div style="font-size:10px;color:var(--muted);margin-top:1px">Spend ${fmtB(TK_ADSSPEND[i])} → Rev ${fmtB(TK_REV[i])}</div>
    </div>`).join('');
  document.getElementById('tk-ads-tb').innerHTML=M5.map((m,i)=>
    `<tr${i===M5.length-1?' class="hl"':''}><td>${m}</td><td>${fmtB(TK_ADSSPEND[i])}</td><td>${fmtB(TK_FEECOMM[i])}</td><td>${tkR[i]}×</td></tr>`
  ).join('');
  const combR=SH_REV.map((v,i)=>+((v+TK_REV[i])/(SH_ADS[i]+TK_ADSSPEND[i])).toFixed(2));
  const maxC=Math.max(...combR);
  document.getElementById('comb-bars').innerHTML=M5.map((m,i)=>`
    <div style="margin-bottom:8px">
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px">
        <span>${m}</span>
        <span><span style="color:var(--sh)">${shR[i]}×</span> · <span>${tkR[i]}×</span> · <b style="color:var(--bl)">${combR[i]}×</b></span>
      </div>
      <div class="bar-bg"><div class="bar-fill" style="width:${Math.round(combR[i]/maxC*100)}%;background:var(--bl)"></div></div>
    </div>`).join('');
}

// ════════════════════════════════════════
// TIKTOK CONTENT
// ════════════════════════════════════════
let ttMo=3;
function setTT(mo,el){
  ttMo=mo;
  document.querySelectorAll('#tt-mo-tabs .mtab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  renderTT();
}
let smInited=false;
function renderTT(){
  const folLast=TK_FOL.length-1;
  const folCur=TK_FOL[folLast],folPrev=TK_FOL[folLast-1],folJan=TK_FOL[0];
  const folMoM=folCur-folPrev,folTotal=folCur-folJan;
  document.getElementById('tt-fol-kpi').innerHTML=`
    <div class="kc" style="padding:9px"><div class="kc-lbl">TK Followers</div><div class="kc-val" style="font-size:15px">${fmtN(folCur)}</div><div class="kc-sub">ปัจจุบัน</div></div>
    <div class="kc" style="padding:9px"><div class="kc-lbl">+เดือนนี้</div><div class="kc-val" style="font-size:15px;color:var(--green)">+${fmtN(folMoM)}</div><div class="kc-sub">จาก ${FOL_M[folLast-1]}</div></div>
    <div class="kc" style="padding:9px"><div class="kc-lbl">ม.ค.→${FOL_M[folLast]}</div><div class="kc-val" style="font-size:15px;color:var(--green)">+${fmtN(folTotal)}</div><div class="kc-sub">${TK_FOL.length} เดือน</div></div>`;
  if(!smInited){
    smInited=true;
    const maxF=Math.max(...TK_FOL);
    document.getElementById('sm-fol-chart').innerHTML=`
      <div class="card" style="margin-bottom:10px">
        <div class="sec-title">TikTok Followers รายเดือน</div>
        ${FOL_M.map((m,i)=>`
          <div style="margin-bottom:8px">
            <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px">
              <span style="font-weight:600">${m}${i===FOL_M.length-1?'<span style="font-size:10px;color:var(--muted)"> (บางส่วน)</span>':''}</span>
              <span style="font-weight:700;color:var(--bl)">${fmtN(TK_FOL[i])}
                ${i>0?`<span style="color:var(--green);font-size:10px"> +${fmtN(TK_FOL[i]-TK_FOL[i-1])}</span>`:''}
              </span>
            </div>
            <div class="bar-bg" style="height:8px"><div class="bar-fill" style="width:${Math.round(TK_FOL[i]/maxF*100)}%;background:${i===FOL_M.length-1?'var(--bl)':'#111'}"></div></div>
          </div>`).join('')}
      </div>`;
    const pillars={};
    ALL_POSTS.forEach(p=>{pillars[p.pillar]=(pillars[p.pillar]||0)+1;});
    const pList=Object.entries(pillars).sort((a,b)=>b[1]-a[1]);
    const totP=ALL_POSTS.length;
    const totV=ALL_POSTS.reduce((a,p)=>a+p.views,0);
    const avgER=(ALL_POSTS.reduce((a,p)=>a+p.er,0)/totP).toFixed(2);
    document.getElementById('sm-pillar').innerHTML=`
      <div class="card" style="margin-bottom:10px">
        <div class="sec-title">Content Overview (มี.ค.–ก.ค.)</div>
        <div class="kgrid" style="margin-bottom:10px">
          <div class="kc"><div class="kc-lbl">Views รวม</div><div class="kc-val">${fmtN(totV)}</div><div class="kc-sub">${totP} คลิป</div></div>
          <div class="kc"><div class="kc-lbl">ER% เฉลี่ย</div><div class="kc-val">${avgER}%</div><div class="kc-sub">เป้า 5%</div></div>
        </div>
        ${pList.map(([p,n])=>`
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px">
            <span class="cpill ${pillCls(p)}" style="flex-shrink:0;min-width:60px;text-align:center">${p}</span>
            <div class="bar-bg" style="flex:1;margin:0;height:6px"><div class="bar-fill" style="width:${Math.round(n/totP*100)}%;background:var(--bl)"></div></div>
            <span style="font-size:11px;font-weight:700;min-width:36px;text-align:right">${n} คลิป</span>
          </div>`).join('')}
      </div>`;}

  const posts=ALL_POSTS.filter(p=>p.m===ttMo);
  if(!posts.length)return;
  const totV=posts.reduce((a,p)=>a+p.views,0);
  const avgRet=(posts.reduce((a,p)=>a+p.ret,0)/posts.length).toFixed(1);
  const avgEr=(posts.reduce((a,p)=>a+p.er,0)/posts.length).toFixed(2);
  const col=mColor[ttMo];
  document.getElementById('tt-kpi').innerHTML=`
    <div class="kc" style="padding:9px"><div class="kc-lbl">Views รวม</div><div class="kc-val" style="font-size:15px">${fmtN(totV)}</div><div class="kc-sub">${posts.length} คลิป</div></div>
    <div class="kc" style="padding:9px"><div class="kc-lbl">5s Ret เฉลี่ย</div><div class="kc-val" style="font-size:15px;color:${+avgRet>=40?'var(--green)':'var(--yellow)'}">${avgRet}%</div><div class="kc-sub">เป้า 40%</div></div>
    <div class="kc" style="padding:9px"><div class="kc-lbl">ER% เฉลี่ย</div><div class="kc-val" style="font-size:15px;color:${+avgEr>=5?'var(--green)':'var(--bl)'}">${avgEr}%</div><div class="kc-sub">เป้า 5%</div></div>`;
  document.getElementById('tt-clips').innerHTML=posts.map(p=>{
    const retCls=p.ret>=40?'good':p.ret<25?'bad':'';
    const wCls=p.watch>=20?'good':p.watch<12?'bad':'';
    const eCls=p.er>=5?'good':p.er<1?'bad':'';
    return`<div class="clip-card">
      <div class="clip-top">
        <div class="clip-day" style="background:${col}">${p.lbl}</div>
        <div style="flex:1">
          <span class="cpill ${pillCls(p.pillar)}">${p.pillar}</span>
          <div class="clip-content">${p.c}</div>
        </div>
      </div>
      <div class="clip-metrics">
        <div class="cm"><div class="cm-val">${fmtN(p.views)}</div><div class="cm-lbl">Views</div></div>
        <div class="cm ${retCls}"><div class="cm-val">${p.ret}%</div><div class="cm-lbl">5s Ret</div></div>
        <div class="cm ${wCls}"><div class="cm-val">${p.watch}%</div><div class="cm-lbl">Watch%</div></div>
        <div class="cm ${eCls}"><div class="cm-val">${p.er}%</div><div class="cm-lbl">ER%</div></div>
      </div>
      ${p.url?`<a href="${p.url}" target="_blank" class="cm-link">ดูคลิป ↗</a>`:''}
    </div>`;}).join('');
}

// ════════════════════════════════════════
// HEADER DATE
// ════════════════════════════════════════
(function(){
  const d=new Date();
  const days=['อาทิตย์','จันทร์','อังคาร','พุธ','พฤหัส','ศุกร์','เสาร์'];
  const mos=['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.'];
  document.getElementById('hdrDate').textContent=`${days[d.getDay()]} ${d.getDate()} ${mos[d.getMonth()]} ${d.getFullYear()+543}`;
})();

// ════════════════════════════════════════
// INIT
// ════════════════════════════════════════
initHome();
initSalesOv();
renderPlt(0);
renderProds();
initMoTables();
initMkOv();
renderAfi();
initAds();
renderTT();
