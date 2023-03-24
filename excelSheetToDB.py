


def readExcelToDB(init_data_path: str) -> bool | None:
    """초기 데이터 추가."""
    setup_logger(__name__.split(".")[0]).info("아니 후 .,.")
    if not os.path.exists(init_data_path):
        return
    excel_file = pd.ExcelFile(init_data_path)
    with SessionLocal() as session:
        for sheet_name in excel_file.sheet_names:
            class_name = sheet_name

            model = getattr(models, class_name)
            records = session.query(model).all()

            log.info(f"inserting datas to '{model.__tablename__}'...", end=" ")

            # 이미 데이터가 있으면 추가 X
            if len(records) == 0:
                df = excel_file.parse(sheet_name)
                df = df.replace({" ": None, np.nan: None})
                for _, data in df.iterrows():
                    session.add(model(**data))
                    session.commit()
                log.info("complete")
            else:
                log.info("pass")

    # for sheet_name in sheet_names:
    #     df = excel_file.parse(sheet_name)
    #     dataframes.append(df)
    #     res = df.to_sql(name=sheet_name, con=engine, if_exists='replace', index=False)
    #     print(df, "@@@", res)
    return True

