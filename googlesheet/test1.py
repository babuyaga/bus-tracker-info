import gspread

sa = gspread.service_account(filename="bttrack-ca98b5f7a1a1.json")
sh = sa.open("VehicleData")

wks = sh.worksheet("Sheet1")

print('Rows:',wks.row_count)
print('Columns:',wks.col_count)

print(wks.acell('a9').value)
print(wks.cell(3,4).value)

print(wks.get('A7:E9'))

print(wks.get_all_records())

print(wks.get_all_values())

wks.update('A3',"Anthony")


# wks.update('D2:E3',[['business','engineering'],['tennis','pottery']])

# wks.update('F2','=UPPER(E2)',raw=False)

# wks.delete_rows(25)