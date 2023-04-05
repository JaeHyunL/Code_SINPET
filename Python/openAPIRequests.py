import urllib.parse
import requests
import json

from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus

from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timedelta

from app.bossLogging import setLog
from app.schemas import WeatherDailyInput
from app.db.session import SessionLocal
from app.models import Weather_grid_location, Weather_Live_Info, Whthr_meta_info_e, Wthr_info_e
from app.core.celery_app import celery_app


def openapi_requests(url=None, parameter='?', **kwagrs) -> dict[str, dict]:
    """공공 API 요청 폼

    Args:
        url ([type], optional): url. Defaults to None.
        parameter (str, optional): 명세 파라미터. Defaults to '?'.

    Returns:
        Dict[str, dict]: 요청 결과
    """
    temp_dict = {}
    for i in kwagrs:
        temp_dict[quote_plus(i)] = kwagrs[i]

    queryParams = parameter + urlencode(temp_dict)
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'

    try:
        response_body = urlopen(request).read().decode('utf-8')
    except Exception as e:
        return e

    return response_body


class Weather:
    """ 기상정보 수집 """
    # TODO 페이징 처리.
    def __init__(self, platform: str, target: str,
                 dataType: str = "json",
                 numOfRows: str = 999,
                 pageNo: int = 1):

        if not platform:
            raise Exception

        self.decodingKey = "bMkM/SABk+ZWxCygmK/jiC1l0m/cEOA5SWWYGGM4IJNBVoJCjxKGhz9LXSXL9lnDIxP/hmHc2/3Tyfdbk2p2Hg=="
        self.url = "http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"
        self.dataType = dataType
        self.numOfRows = numOfRows
        self.pageNo = pageNo

    def asos_request(
        self, dataCd: str = 'ASOS',
        dateCd: str = 'DAY',
        startDt: int = None,
        endDt: int = None,
        stnIds: int = None) -> bool | None:
        """ ASOS 종관 데이터 요청 및 등록

        Args:
            dataCd (str, optional): 데이터 코드. Defaults to 'ASOS'.
            dateCd (str, optional): 데이트 코드. Defaults to 'DAY'.
            startDt (int, optional): 시작 날짜. Defaults to None.
            endDt (int, optional): 종료 날짜. Defaults to None.
            stnIds (int, optional): 지점 번호. Defaults to None.

        Returns:
            bool: 성공/실패self.__dict__,
        """

        try:
            values = openapi_requests(
                url=self.url,
                ServiceKey=self.decodingKey,
                dataType=self.dataType,
                numOfRows=self.numOfRows,
                pageNo=self.pageNo,
                dataCd=dataCd,
                dateCd=dateCd,
                startDt=startDt,
                endDt=endDt,
                stnIds=stnIds
            )
            values = json.loads(values)
        except Exception:
            return False
        try:
            values = values['response']['body']['items']['item']
        except Exception as e:
            setLog(__name__).debug(f'Location {stnIds}No Response {e}')
            return False

        with SessionLocal() as session:

            for value in values:
                value['id'] = "WT" + str(value['tm']).replace("-", "") + str(int(stnIds)).zfill(3)
                session.add(Wthr_info_e(**WeatherDailyInput(**value).dict()))
                try:
                    session.commit()
                except Exception as e:
                    print("중복키 방어 커낵션 풀 ", e)
                    session.rollback()
                    continue

        return True


@celery_app.task(bind=True, name="boss.schedule.weather")
def requestsWeather(
    self,
    serviceKey: str = 'Xh6HpMuO2+cJDqhshrjEyFN142XEX+AMShiD/Q701ifft3pXxGGEx7kv/Nu3NTP/YWCGG1B97fJA8/LEO0Ehww==',  # noqa
    reqUrl = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst',  # noqa
):
    """공공데이터포털 기상청 예보 조회 API

    Args:
        url (http): 공공데이터 포털 요청 URL.
        serviceKey (str): 디코딩 key.
    """
    vilageFcstURL = reqUrl

    params = {
        'serviceKey': serviceKey,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'json',
        'base_date': '20210628',
        'base_time': '0600',
        'nx': '55',
        'ny': '127'
    }
    with SessionLocal() as session:

        res = session.query(
            Weather_grid_location.nx,
            Weather_grid_location.ny).all()
        requestTime = datetime.now()
        for nx, ny in list(set(res)):
            params['nx'] = nx
            params['ny'] = ny
            params['base_date'] = datetime.now().strftime("%Y%m%d")
            params['base_time'] = requestTime.strftime("%H%M")
            try:
                responseULFSCT = eval(requests.get(vilageFcstURL, params=params).text)
                responses = responseULFSCT['response']['body']['items']['item']
            except Exception:
                continue

            for response in responses:
                response['weatherKindCode'] = "003"
                response['id'] = response['fcstDate'] + response['fcstTime']
                response['id'] += response['category'] + str(response['nx'])
                response['id'] += str(response['ny']) + response['weatherKindCode']
                response['updated_at'] = datetime.now()
                stmt = insert(Weather_Live_Info).values(
                    **response
                ).on_conflict_do_update(
                    index_elements=['id'],
                    set_=response
                )
                session.execute(stmt)
                session.commit()


@celery_app.task(bind=True, name="boss.external.wth_info_register")
def asos_request_service(
    self,
    startDt: str | None = None,
    endDt: str | None = None,
    stnIds="*"
):
    if not startDt:
        startDt = datetime.strftime(
            datetime.now() - timedelta(days=1),
            "%Y%m%d")
    if not endDt:
        endDt = datetime.strftime(
            datetime.now() - timedelta(days=1),
            "%Y%m%d")

    with SessionLocal() as session:
        qur = session.query(Whthr_meta_info_e.loc_id).all()
    print('st', startDt, '#####')
    st = datetime.strptime(startDt, "%Y%m%d")
    et = datetime.strptime(endDt, "%Y%m%d")

    tm = (et - st).days // 999

    for i in range(tm + 1):

        wth = Weather("AsosDalyInfoService", "getWthrDataList", pageNo=i + 1)
        if not stnIds or stnIds == "*":
            for loc, *others in qur:
                result = wth.asos_request(
                    startDt=startDt,
                    endDt=endDt,
                    stnIds=int(loc))

        else:

            result = wth.asos_request(
                startDt=startDt,
                endDt=endDt,
                stnIds=stnIds
            )

    return result


# asos_request_service(startDt='19500101', endDt='20230403', stnIds="*")
