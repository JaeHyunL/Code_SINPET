


def creation_date(path_to_file: str) -> time:
    """
    파일 생성시간 추출 메서드

    Args:
        path_to_file (str): 파일 경로

    Returns:
        time: 파일 생성날짜
    """
    if platform.system() == 'Windows':
        return time.ctime(os.path.getctime(path_to_file))
    else:
        stat = os.stat(path_to_file)
        try:
            return time.ctime(stat.st_birthtime)
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return time.ctime(stat.st_mtime)


def meta_info_init(filename: str = 'asos-meta-info.xlsx') -> bool:
    """
    기상청 메타 정보 등록 로직(whthrmetainfo, tl_scco_emd)

    Args:
        filename (str): meta정보 엑셀 위치 등록 'asos-meta-info.xlsx'.

    Returns:
        bool: bool
    """
    data_path = os.path.join("/datadrive/config/teplates", filename)
    if not os.path.exists(data_path):
        setLog(__name__).debug('meta file Not Found')
        return False

    xl = pd.ExcelFile(data_path, engine='openpyxl')

    with SessionLocal() as session:
        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name)
            emd_list = []
            # TODO 반복문 줄일 수 있는 방법 고려.
            for index, loc_id, lon, lat, *others in df.to_records():
                print(loc_id)
                # 해당 포인트가 속한 바운더리 추출
                emd_info = session.query(Tl_emd.emd_cd).filter(func.ST_Contains(
                    func.ST_Transform(Tl_emd.wkb_geometry, 4326),
                    func.ST_SetSRID(func.ST_Point(lon, lat), 4326)
                ))
                print(emd_info.all()[0][0])
                try:
                    emd_list.append(emd_info.all()[0][0])  # TODO 시각적 잡음 해결
                except IndexError:
                    setLog(__name__).debug(f"Parser Indexing Exception {loc_id} // {others}")
                    emd_list.append(None)

            df = df.reset_index(drop=True)
            df['emd_cd'] = pd.Series(emd_list)
            df['acq_dt'] = creation_date(data_path)
            df = df.to_dict(orient='records')

            stmt = insert(Whthr_meta_info_e).values(
                df
            )
            session.execute(stmt)

    return True
