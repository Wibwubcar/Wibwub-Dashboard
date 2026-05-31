/**
 * WIBWUB HR — Google Apps Script
 * รับข้อมูลเช็คอิน/ใบลา แล้วเขียนลง Google Sheet
 *
 * วิธีติดตั้ง:
 * 1. ไปที่ script.google.com → New project
 * 2. วางโค้ดทั้งหมดนี้ลงไป
 * 3. Deploy → New Deployment → Web App
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 4. Copy URL แล้วใส่ใน Mobile App → HR → ตั้งค่า → GAS Sheets URL
 */

// ── CONFIG ──────────────────────────────────────────────────────
// ถ้าต้องการระบุ Spreadsheet ID ตรงๆ ให้ใส่ที่นี่
// ถ้าเว้นว่าง ระบบจะสร้างไฟล์ใหม่ในโฟลเดอร์รูทของ Drive
const SPREADSHEET_ID = ''; // ← ใส่ ID ของ Sheet ที่อยู่ใน Data checkin ถ้ามีแล้ว

const SHEET_NAMES = {
  attendance:    'เช็คอิน-เช็คเอาท์',
  leave_request: 'ใบลา',
  leave_update:  'ใบลา',   // update สถานะในชีทเดิม
};

// ── HEADERS ─────────────────────────────────────────────────────
const ATTENDANCE_HEADERS = [
  'วันที่','UID','ชื่อ','Email','แผนก/Role',
  'เวลาเข้างาน','เวลาออกงาน','ชั่วโมง','สถานะ',
  'Lat (เข้า)','Lng (เข้า)','บันทึกเมื่อ'
];

const LEAVE_HEADERS = [
  'วันที่ยื่น','UID','ชื่อ','Email','แผนก/Role',
  'ประเภทลา','วันเริ่ม','วันสิ้นสุด','จำนวนวัน','เหตุผล',
  'สถานะ','ผู้อนุมัติ','วันที่อนุมัติ','หมายเหตุ'
];

// ── MAIN ─────────────────────────────────────────────────────────
function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    const type = body.type;   // 'attendance' | 'leave_request' | 'leave_update'
    const data = body.data;

    const ss = getOrCreateSpreadsheet();

    if (type === 'attendance') {
      writeAttendance(ss, data);
    } else if (type === 'leave_request') {
      writeLeave(ss, data);
    } else if (type === 'leave_update') {
      updateLeaveStatus(ss, data);
    }

    return reply({ ok: true, type: type });
  } catch (err) {
    return reply({ ok: false, error: err.message });
  }
}

function doGet(e) {
  return reply({ ok: true, status: 'WIBWUB HR Sheets Proxy OK' });
}

// ── HELPERS ──────────────────────────────────────────────────────
function getOrCreateSpreadsheet() {
  if (SPREADSHEET_ID) {
    return SpreadsheetApp.openById(SPREADSHEET_ID);
  }
  // หาไฟล์ชื่อ WIBWUB_HR_Data ใน Drive
  const files = DriveApp.getFilesByName('WIBWUB_HR_Data');
  if (files.hasNext()) {
    return SpreadsheetApp.openById(files.next().getId());
  }
  // สร้างใหม่
  const ss = SpreadsheetApp.create('WIBWUB_HR_Data');
  ss.getActiveSheet().setName('README');
  ss.getActiveSheet().getRange('A1').setValue('WIBWUB HR Data — สร้างโดยอัตโนมัติ');
  return ss;
}

function getOrCreateSheet(ss, sheetName, headers) {
  let sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
    // ใส่ header
    const headerRange = sheet.getRange(1, 1, 1, headers.length);
    headerRange.setValues([headers]);
    headerRange.setFontWeight('bold');
    headerRange.setBackground('#1A5CDB');
    headerRange.setFontColor('#ffffff');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function fmtDateTime(isoStr) {
  if (!isoStr) return '';
  try {
    const d = new Date(isoStr);
    return Utilities.formatDate(d, 'Asia/Bangkok', 'dd/MM/yyyy HH:mm:ss');
  } catch(e) { return isoStr; }
}

function fmtDate(isoStr) {
  if (!isoStr) return '';
  try {
    const d = new Date(isoStr);
    return Utilities.formatDate(d, 'Asia/Bangkok', 'dd/MM/yyyy');
  } catch(e) { return isoStr; }
}

// ── ATTENDANCE ────────────────────────────────────────────────────
function writeAttendance(ss, d) {
  const sheet = getOrCreateSheet(ss, SHEET_NAMES.attendance, ATTENDANCE_HEADERS);

  // ค้นหา row เดิมของ uid+date
  const uid   = d.uid   || '';
  const date  = d.date  || '';
  const docId = uid + '_' + date;

  const lastRow = sheet.getLastRow();
  let existingRow = -1;

  if (lastRow > 1) {
    // ค้นหาใน column B (UID) และ column A (วันที่)
    const dataRange = sheet.getRange(2, 1, lastRow - 1, 2).getValues();
    for (let i = 0; i < dataRange.length; i++) {
      if (dataRange[i][0] === date && dataRange[i][1] === uid) {
        existingRow = i + 2;
        break;
      }
    }
  }

  const row = [
    date,
    uid,
    d.name  || '',
    d.email || '',
    d.dept  || '',
    fmtDateTime(d.check_in),
    fmtDateTime(d.check_out),
    d.work_hours || '',
    d.status || '',
    d.check_in_lat  || '',
    d.check_in_lng  || '',
    fmtDateTime(new Date().toISOString()),
  ];

  if (existingRow > 0) {
    // อัปเดต row เดิม
    sheet.getRange(existingRow, 1, 1, row.length).setValues([row]);
  } else {
    // เพิ่ม row ใหม่
    sheet.appendRow(row);
    // สีแถว สลับ
    const newRow = sheet.getLastRow();
    if (newRow % 2 === 0) {
      sheet.getRange(newRow, 1, 1, row.length).setBackground('#f0f4ff');
    }
  }
}

// ── LEAVE ─────────────────────────────────────────────────────────
function writeLeave(ss, d) {
  const sheet = getOrCreateSheet(ss, SHEET_NAMES.leave_request, LEAVE_HEADERS);
  const row = [
    fmtDate(d.created_at || new Date().toISOString()),
    d.uid    || '',
    d.name   || '',
    d.email  || '',
    d.dept   || '',
    d.type   || '',
    d.start_date || '',
    d.end_date   || '',
    d.days   || '',
    d.reason || '',
    'รอพิจารณา',
    '',
    '',
    '',
  ];
  sheet.appendRow(row);
  const newRow = sheet.getLastRow();
  if (newRow % 2 === 0) {
    sheet.getRange(newRow, 1, 1, row.length).setBackground('#fffbeb');
  }
}

function updateLeaveStatus(ss, d) {
  const sheet = getOrCreateSheet(ss, SHEET_NAMES.leave_update, LEAVE_HEADERS);
  const uid = d.uid || '';
  const startDate = d.start_date || '';
  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return;

  const dataRange = sheet.getRange(2, 2, lastRow - 1, 7).getValues();
  for (let i = 0; i < dataRange.length; i++) {
    // column B=uid, column G=start_date (index 5)
    if (dataRange[i][0] === uid && dataRange[i][5] === startDate) {
      const targetRow = i + 2;
      sheet.getRange(targetRow, 11).setValue(d.status || '');         // สถานะ
      sheet.getRange(targetRow, 12).setValue(d.approved_by || '');    // ผู้อนุมัติ
      sheet.getRange(targetRow, 13).setValue(fmtDateTime(d.approved_at || '')); // วันที่อนุมัติ
      sheet.getRange(targetRow, 14).setValue(d.admin_note || '');     // หมายเหตุ
      // ไฮไลต์สีตามสถานะ
      const color = d.status === 'approved' ? '#dcfce7' : d.status === 'rejected' ? '#fee2e2' : '#fffbeb';
      sheet.getRange(targetRow, 1, 1, 14).setBackground(color);
      break;
    }
  }
}

function reply(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
