#!/usr/bin/env bash

echo "Make sure you activated the virtualenv or have an alias for python3 named 'python'."
echo "Make sure the requirements in 'requirements.txt' are satisfied."
echo "Finally, make sure your prompt is placed in 'scripts' directory."

echo "daily_count script started..."
python daily_count.py
echo "daily_count script done!!!\n"

echo "daily_count_normalized script started..."
python daily_count_normalized.py
echo "daily_count_normalized script done!!!\n"

echo "new_clients script started..."
python new_clients.py
echo "new_clients script done!!!\n"

echo "success_by_hour script started..."
python success_by_hour.py
echo "success_by_hour script done!!!"

echo "generate_30_parcels_data script started..."
python generate_30_parcels_data.py
echo "generate_30_parcels_data script done!!!"

echo "30_parcels_daily_count script started..."
python 30_parcels_daily_count.py
echo "30_parcels_daily_count script done!!!"
