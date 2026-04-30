import json
import os
import glob
import sys
import time

sys.path.insert(0, '/home/slawsky/taxappfiles')
os.chdir('/home/slawsky/taxappfiles')

import createCodeAndRegsImages as cc

def process_pending_jobs():
    job_files = glob.glob('saved_code/job.*.json')
    
    for job_path in job_files:
        status_path = None
        try:
            with open(job_path, 'r') as f:
                job = json.load(f)
            
            os.remove(job_path)
            
            status_path = f"saved_code/status.{job['now']}.json"
            
            all_errors, footer_error = cc.create_code_book(
                job['book_title'],
                job['excel_path'],
                job['now'],
                job['docsdropdown'],
                job['pagenumber']
            )
            
            with open(status_path, 'w') as f:
                json.dump({
                    "status": "done",
                    "all_errors": all_errors or "",
                    "footer_error": footer_error or "",
                    "book_title": job['book_title']
                }, f)
                
        except Exception as e:
            import traceback
            if status_path:
                with open(status_path, 'w') as f:
                    json.dump({
                        "status": "error",
                        "message": str(e),
                        "traceback": traceback.format_exc()
                    }, f)

if __name__ == "__main__":
    while True:
        process_pending_jobs()
        time.sleep(5)  # check every 5 seconds
