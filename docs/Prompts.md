python deployment/remote.py --create_session --resource_id 4132633200251895808 --user_id kg

python deployment/remote.py --list

python deployment/remote.py --create


python deployment/remote.py --list_sessions --resource_id 4132633200251895808 --user_id kg

python deployment/remote.py --send --resource_id 4132633200251895808 --session_id 1027289656749719552 --user_id kg --message "provide the list of corporas"


python deployment/remote.py --send --resource_id 4132633200251895808 --session_id 1027289656749719552 --user_id kg --message "I would like to create new knowledge store called Research"


python deployment/remote.py --send --resource_id 4132633200251895808 --session_id 1027289656749719552 --user_id kg --message "I would like to add the following doc to my business corpus:gs://ragagentmain12222025/RagFiles/DeepSeek-AI et al. - 2025 - DeepSeek-V3 Technical Report.pdf"


python deployment/remote.py --send --resource_id 4132633200251895808 --session_id 1027289656749719552 --user_id kg --message "What do they talk about in section 2 in DeepSeek-V3 Technical Report.pdf"
