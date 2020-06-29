python -m firststreet -p location.get_detail
python -m firststreet -p adaptation.get_detail -i 39
python -m firststreet -p adaptation.get_detail -i p
python -m firststreet -p adaptation.get_detail -i p,39
python -m firststreet -p adaptation.get_detail -i 39 -v v2
python -m firststreet -p location.get_detail -f .\tests\data_text\sample.txt
python -m firststreet -p location.get_detail -f .\tests\data_text\sample.txt -l property
python -m firststreet -p adaptation.get_detail -limit 1
python -m firststreet -p location.get_detail -f .\tests\sam.txt -l property -limit 1
python -m firststreet -p adaptation.get_detail -i 39 -log True
python -m firststreet -p adaptation.get_detail -i 39 -log False
python -m firststreet -p adaptation.get_details_by_location -i 3807200 -l city -log True
python -m firststreet -p historic.get_events_by_location -i 3807200 -l city -log False