"""Deactivate the 10 duplicate pack products created in error (the canonical,
already-documented copies stay live)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sd_session import fetch

HDR = {'origin': 'https://stabledeliver.com',
       'referer': 'https://stabledeliver.com/dashboard/products'}

DUPES = [
    'cf10ac7b-ce34-45bc-9010-552d3cf27bd7',  # etsy
    '5c4b5509-da11-422d-a6f4-1645b61f85c9',  # realestate
    '9f1bfa21-36c8-4651-bfde-84c26c8d6047',  # video
    '4a26b6af-38f7-407e-a8af-7b93d625e6bc',  # career
    '86a34c9f-de3d-49be-b6ff-021055a6e324',  # fitness
    '35e3e07d-dfcb-4747-a273-8a15a1a1ddc0',  # fashion
    'c9677c6e-b1e8-4557-a244-5ff545e9b1d8',  # saas
    'ffb488d7-5cdd-4a5c-b846-3d656f37ec06',  # creative
    '60d2ca89-7cce-4d32-bb4a-223d0bfe4d2b',  # ecommerce
    '2538fbbb-1834-448c-a00d-408e56591d66',  # food
]

for pid in DUPES:
    st, resp, _, _ = fetch('/api/dashboard/products/' + pid, method='PATCH',
                           data={'active': False}, headers=HDR)
    print(st, resp, pid)
