import shapefile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mymodels import MyModel  # mymodels는 사용자 정의 모델 파일입니다.

# 데이터베이스 연결 설정
engine = create_engine('postgresql://user:password@localhost/mydatabase')
Session = sessionmaker(bind=engine)
session = Session()

# shp 파일 읽기
sf = shapefile.Reader('path/to/myfile.shp')

# shp 파일의 각 feature를 순회하며 데이터베이스에 저장
for shape_rec in sf.shapeRecords():
    # MyModel 객체 생성
    mymodel = MyModel()
    # MyModel 객체에 필드값 할당
    mymodel.field1 = shape_rec.record[0]
    mymodel.field2 = shape_rec.record[1]
    mymodel.field3 = shape_rec.record[2]
    # 좌표값 할당
    mymodel.latitude = shape_rec.shape.points[0][1]
    mymodel.longitude = shape_rec.shape.points[0][0]
    # 데이터베이스에 저장
    session.add(mymodel)

# 변경 사항 커밋
session.commit()

# 세션 닫기
session.close()
