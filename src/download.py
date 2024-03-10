import os

import gdown
import requests
from megapy import Mega

from src.site import get_filename_to_save


def download_from_url(
    download_url: str, download_folder: str, title: str, media_type: str
):
    if "mega.nz" in download_url:
        filename = get_filename_to_save(title, media_type)
        if filename is None:
            raise ValueError(
                f"Media type: {media_type} is not supported while getting filename to save."
            )
        download_mega(download_url, download_folder, filename)
    elif "drive.google.com" in download_url:
        filename = get_filename_to_save(title, media_type)
        if filename is None:
            raise ValueError(
                f"Media type: {media_type} is not supported while getting filename to save."
            )
        download_gdrive(download_url, download_folder, filename)
    elif "onedrive.live.com" in download_url:
        filename = get_filename_to_save(title, media_type)
        if filename is None:
            raise ValueError(
                f"Media type: {media_type} is not supported while getting filename to save."
            )
        download_onedrive(download_url, download_folder, filename)
    else:
        raise ValueError("The download_url is not supported.")


def download_mega(download_url: str, download_folder: str, filename: str):
    """Download the file from the download_url and save it to the download_folder."""
    mega = Mega()
    file_path = os.path.join(download_folder, filename)
    mega.download_url(download_url, file_path, ignore_quota_warn=True)


def download_gdrive(download_url: str, download_folder: str, filename: str):
    """Download the file from the download_url and save it to the download_folder."""
    file_path = os.path.join(download_folder, filename)
    gdown.download(download_url, file_path)


def download_onedrive(onedrive_url: str, download_folder: str, filename: str):
    """Download the file from the download_url and save it to the download_folder."""
    file_path = os.path.join(download_folder, filename)

    onedrive_url = onedrive_url.replace("amp;", "")

    download_url = ONEDRIVE_MAP.get(onedrive_url, None)
    if download_url is None:
        raise ValueError(
            "Downloading from OneDrive is only supported to certain URLs that are already mapped."
        )
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)


# Map of the OneDrive URLs to download URLs
# I hate MS
ONEDRIVE_MAP = {
    "https://onedrive.live.com/?authkey=%21ADMpXy0JU4cd05Q&cid=4143864FC4132B6D&id=4143864FC4132B6D%211033&parId=4143864FC4132B6D%211032&o=OneUp": "https://jwtyng.by.files.1drv.com/y4mFAxeurLFnn2YW-v8O5chZW0c7zF6Eja2TOv5Tii_oquZLaJGl2pST0eXCcMgiN9IlOPUnT2xvhc4Y3xXs4oqrv0xtKAILmo9wSrKx-6oFToE7x-tglDgUX8JsjLNPFw2L9nX2i1UX_3ql8HnltffcAGymFaheLMxhlnBI7gOYno-qQ_G_cNDNfE4lrwLv6R5iQ-HtMPcK6auWjXlzSQoOJ1rvUWGSYY873qbQUkMpzg",
    "https://onedrive.live.com/?authkey=%21AAb9WNsuSFa489k&cid=4143864FC4132B6D&id=4143864FC4132B6D%211034&parId=4143864FC4132B6D%211032&o=OneUp": "https://katyng.by.files.1drv.com/y4mHtPZwfTpYOmsKGvn_knCAuYufK_G0XMRen_LsIG2jkBbtFkV2TUghy94YHzgSIFrn-Vs40l3N9hXA-4sEIoLLzHH9aLjuIa3oMYwgtYkmPL16YRTksrwsmGcAgxBncGrWw7QsEugBSg6lSgu1JLmybGK4huT3zqZ912_T7S9Ow6nAG3p1FCIqQSi2AFizCeadwXZ28m6-LWOtosAwz1to5wsL5iuJ8e39U7ociCAjZs",
    "https://onedrive.live.com/?authkey=%21AL%2DfzgFDBS3aQyM&cid=4143864FC4132B6D&id=4143864FC4132B6D%211035&parId=4143864FC4132B6D%211032&o=OneUp": "https://kqtyng.by.files.1drv.com/y4mxQaA2rHEY15Gf41fBc2cmJBlAFp9cR_4QSuzRui4KF-K6FpEoLGuNHuaidJqsFL6XgI01ro8HLBbsczoAyyF-nFD7Zz9w9_WsQFUXYu7bo8Kgk99EKPBOm6cubNtCVTuJEFI7cG4PL2aV1Ddn6SchToT4cyadshRHsrsolQXiP8Sz4DhdvqZbB3pADpjTrTL2Pa53B0e-oI6YY_TRuUEfTMLcTFHjcu_BR-26j-sHLY",
    "https://onedrive.live.com/?authkey=%21AGe%2Djf6EghTBbhk&cid=4143864FC4132B6D&id=4143864FC4132B6D%211036&parId=4143864FC4132B6D%211032&o=OneUp": "https://kgtyng.by.files.1drv.com/y4mTBPduriGoMYbPqm3LvvK2jQyW4-UEaMCpQ9TkX1pwA-WM-d-KJ2Vnc2v1jklWT2tNqXdUsgBlrbhVpgXsFCg_7ezLYrV91Bl2h_Ws_8mTLkK8NeFvlLLmkor9WQVih23qZEVpuquSbMx0-eMsFHvego2Anjvt7BsGmaxvxOsRRp6T3No4EkOXatTwLyeP4nJxv_A9ExzzIDJ_bsumdQcSJJbOUGi3K_n8WV-ppqnaEk",
    "https://onedrive.live.com/?authkey=%21APchE2O31a0Scjs&cid=4143864FC4132B6D&id=4143864FC4132B6D%211037&parId=4143864FC4132B6D%211032&o=OneUp": "https://kwtyng.by.files.1drv.com/y4mDJxO19GRjgY8lHCetJAIgKBpeyHzI4Q4kbXl4pXMoKO7prZuKKdM3Prs_8WASmfzNl3uHe7ctX5R_LfFpEB4-YSpS2kqAnTXaeqaAqxgLA7CC_s5AXhczlwitVNLC6zW0c5yXWPRjVUoXoawgDidhsJyI1g07_N87lClU3rMYLRJkFhwPpxNOhCj_TKc65LZUolrTn6HNi2V5Hmdt96L8fvnU2-2xdnRiMdqRDvE3HI",
    "https://onedrive.live.com/?authkey=%21AIhX3gj%2DhzUgNzI&cid=4143864FC4132B6D&id=4143864FC4132B6D%211038&parId=4143864FC4132B6D%211032&o=OneUp": "https://hatyng.by.files.1drv.com/y4mzpD-KLyM8tzI9VcwxLzVZQyV5W-mRaVzkcR9ee9UbkqNff0ogpdOA3dXXHx2gK06d0PSiqrZyrO9sofALVEDtiBAlh7sGqFzVy9S3-3ETs7Iz-EHVR1WINLeXIw2sTIRACAVOYRU2RxaiujF-mHctNOeW9e2UtRWuVxPAt3i-ssEgO76VwqCEg-xuaRFNYIebOHmXuFAikdrHX059XefAAhFEXdXmeuT3cg__X7GmEQ",
    "https://onedrive.live.com/?authkey=%21APWOQfHOIKk8ZdM&cid=4143864FC4132B6D&id=4143864FC4132B6D%211039&parId=4143864FC4132B6D%211032&o=OneUp": "https://hqtyng.by.files.1drv.com/y4mqKRgKBI_-ABfoCdmuCnyCllnNnCQCu0XWw8EJAhMzIe1olJ923WDY_4Dkr0nSoZm0EWwNDGsaa-fvZpNGT7n2nYNCjLZnJHX_Esjj7tW_6cbUkGf_kimgUbr5K6m2RTHhhlAhEWLdquDbQBOaAnwKyQp7M3yIo_pizxht8WBh5vH41kzxLh124FZt79-CiGYSwOdIhbJOcRW5RKvC4-B32lAq2alCU1i_nHGXUSMGRo",
    "https://onedrive.live.com/?authkey=%21ADsojjHZj9jxpno&cid=4143864FC4132B6D&id=4143864FC4132B6D%211040&parId=4143864FC4132B6D%211032&o=OneUp": "https://jatffq.by.files.1drv.com/y4m5Lvv-EhNd4g4wEgmL-0Hmrndirg7IcXQvK1m_7n37ZLGr3GX93Kh80wJZSJqIGj0VY_PuGlGsqatesH1GSfQOCXmqrvzfi5X4-23HV-ECZ3PgF53xugmLSj8koP7-WClJQ-cfoy4icAuYfTCOuh_4yNeDEeo78b9xxCUduzuPvqaLx2OIwWdIA_aN1-12v9NgoJNCW7oeNa831aeb-IXRVNHd3itz6V3UWO82CMQ0kY",
    "https://onedrive.live.com/?authkey=%21AEDGUBK4CS3DPvc&cid=4143864FC4132B6D&id=4143864FC4132B6D%211041&parId=4143864FC4132B6D%211032&o=OneUp": "https://jqtffq.by.files.1drv.com/y4mN55eDiFLleLt6byNNv8Hs49gq3hwkLbLNMltzqyU_zABtjexgb8oRMtZSeu4QgKhpOfAQOws7RVRcyVs_s3oa48V2Ieb_xZ-7-4ASyt-KTAnhKSvt9wpxl20t3DqgGwAv4KBSZhZn0Sw4ECqCfsRDBtZmGWHJhK8v9JqCbKhVRr0_tuleQqGUPrpE5YHR_g0M--PqR4v6AY3EdXI1g43E9Rt8zkGkWKkMnDUq7M34uc",
    "https://onedrive.live.com/?authkey=%21AJCc%2D9Nci%2Dax6wU&cid=4143864FC4132B6D&id=4143864FC4132B6D%211042&parId=4143864FC4132B6D%211032&o=OneUp": "https://jgtffq.by.files.1drv.com/y4me29njR776cqakHglgQWnZLez-36E-LRplOhLN1D1LVOxdA7e-q5MNz5QR0rWEOnrkZ-sdqu3BNOBmveG1UoQXC9Te6PbIoiQfp2WKNIlLoX0SPQmpslc37bXSW50UmniK5qwsexCiF7kz17UIQXTOvQD7nrHLW2p1p3fBolmiIoMswSSosCQGABkDI_cW8B-01qvizyr4gHKxYceismpaoT-vcLJ79GMyjfoBUpivkY",
    "https://onedrive.live.com/?authkey=%21ADGT5cg8ccJWsYY&cid=4143864FC4132B6D&id=4143864FC4132B6D%211043&parId=4143864FC4132B6D%211032&o=OneUp": "https://jwtffq.by.files.1drv.com/y4moQDGD614b-JTPjpnhcO1kxTUBRfp8KVeTzHoQOwAUf3JhYgn1Cm6j45i3Q-W6qpbyiwo_7x3XIUz2M1XUWPtfx06sKvUcDr8-KOcAyPOZPlUNbJmP3b2heGvDpp7W7ofSwewfEKe0iovZ1Eo2uab7Uh_I6tqWP-v9XODvpNNC-MapotVw7YLXQgU57j4FBNb3gLlDustOreuu0MSXOgK2wt14jGACdb-_AipLkB4DFY",
    "https://onedrive.live.com/?authkey=%21ABYjnFuMCfKJB7g&cid=4143864FC4132B6D&id=4143864FC4132B6D%211046&parId=4143864FC4132B6D%211032&o=OneUp": "https://kgtffq.by.files.1drv.com/y4m39zt5a5tp4UmDNlSkQ1k19giq56ETxjt6DB5QLpH4TJRVJuCL3YawDWruCZGA4AqjSIdgaPHOk57K-1-Gn-MZaGDm_w3RUf1Ykq3u74pSB75EbyNtRUlr-Bk8aMw-xyFYF02LYLAsu_2t93ak3SMRiKuAaWbKcIq3i9IhB6zBWY38BKNpQLgRIaZGFNCC3NJsTFAd3srKSighM2hO91bRdNZmc8FAwj95Rb1vWTyUyM",
    "https://onedrive.live.com/?authkey=%21AGXx7N8v6LojbPM&cid=4143864FC4132B6D&id=4143864FC4132B6D%211047&parId=4143864FC4132B6D%211032&o=OneUp": "https://kwtffq.by.files.1drv.com/y4mbj5iZDMtqf_IqWrLqCGFszY9PZgr1Qi7Q9gajrfSGXWMew0eIdHqsNqjWJ7RqjcQXbe_OrTLPHyAapLmU39oKFvHemdXYyFfK6y6x_HKIXttergaNGulLJH0dzu7WXI5CJXvx0au4rWnojsyQBT3XkX3_4dLoayHir9aFkamykXuuhzxKwa5mOCsOz0hv9FXFFesPWjasHoUbRq-RbRoCj4fCanxw6XRQQFVVLAO-pg",
}
