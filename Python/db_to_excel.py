from sqlalchemy import create_engine
import pandas as pd


engine = create_engine('POSTGRSQL_DSN')

# 데이터베이스의 모든 테이블을 Pandas DataFrame으로 가져오기
dfs = {}
with engine.connect() as connection:
    for table_name in engine.table_names():
        query = f"SELECT * FROM {table_name}"
        dfs[table_name] = pd.read_sql(query, connection)

# print(dfs)

# 결과 확인
# with pd.ExcelWriter('output.xlsx') as writer:  
with pd.ExcelWriter('output2') as writer:  
    for table_name, df in dfs.items():
        try:
            # df.to_excel(writer, sheet_name=table_name)
            df.to_csv(writer, sheet_name=table_name)
        except Exception as e:
            print(e)
            continue

        # df2.to_excel(writer, sheet_name='Sheet_name_2')
    # df.to_excel()
