# ☁️ AWS Deployment Guide – Healthcare Data Platform

## Overview

This guide covers deploying the Healthcare Data Platform to AWS using:
- **Amazon S3** – Store processed data and raw backups
- **Amazon EC2** – Run the ETL pipeline
- **Amazon RDS (MySQL)** – Cloud-hosted MySQL database

---

## 📋 Prerequisites

1. AWS Account with IAM credentials
2. AWS CLI installed and configured
3. Python 3.x with `boto3` installed
4. MySQL client for RDS connection

---

## 🪣 Step 1: Upload Data to S3

### Create S3 Bucket
```bash
aws s3 mb s3://healthcare-data-platform-bucket
```

### Upload Raw Data
```bash
aws s3 sync data/raw/ s3://healthcare-data-platform-bucket/raw/
```

### Upload Processed Data
```bash
aws s3 sync data/processed/ s3://healthcare-data-platform-bucket/processed/
```

### Python Script for S3 Upload
```python
import boto3
import os

s3 = boto3.client('s3')
BUCKET_NAME = 'healthcare-data-platform-bucket'

def upload_folder(local_path, s3_prefix):
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file = os.path.join(root, file)
            s3_key = os.path.join(s3_prefix, os.path.relpath(local_file, local_path))
            s3.upload_file(local_file, BUCKET_NAME, s3_key)
            print(f"Uploaded: {s3_key}")

upload_folder('data/raw', 'raw')
upload_folder('data/processed', 'processed')
```

---

## 🖥 Step 2: Setup EC2 Instance

### Launch EC2 Instance
1. Go to AWS Console → EC2 → Launch Instance
2. Choose **Amazon Linux 2** or **Ubuntu 22.04 LTS**
3. Instance type: **t2.medium** (for PySpark)
4. Configure security group:
   - SSH (port 22) from your IP
   - MySQL (port 3306) from your IP
5. Create/select a key pair

### Connect to EC2
```bash
ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>
```

### Install Dependencies on EC2
```bash
# Update system
sudo yum update -y   # Amazon Linux
# OR
sudo apt update && sudo apt upgrade -y   # Ubuntu

# Install Python and pip
sudo yum install python3 python3-pip -y   # Amazon Linux
# OR
sudo apt install python3 python3-pip -y   # Ubuntu

# Install Java (for PySpark)
sudo yum install java-11-openjdk -y   # Amazon Linux
# OR
sudo apt install openjdk-11-jdk -y   # Ubuntu

# Clone project
git clone <your-repo-url> healthcare-data-platform
cd healthcare-data-platform

# Install Python dependencies
pip3 install -r requirements.txt
```

### Run Pipeline on EC2
```bash
python3 -m src.main
```

---

## 🗄 Step 3: Setup RDS (MySQL)

### Create RDS Instance
1. Go to AWS Console → RDS → Create Database
2. Engine: **MySQL 8.0**
3. Template: **Free Tier** or **Production**
4. DB Instance: **db.t3.micro** (free tier)
5. Set Master username/password
6. Enable public access (for development only)
7. Configure security group to allow MySQL (port 3306)

### Connect to RDS
```bash
mysql -h <RDS-ENDPOINT> -u admin -p
```

### Run Schema Setup
```sql
SOURCE sql/db.sql;
SOURCE sql/schema.sql;
SOURCE sql/procedures.sql;
```

### Update Config
Update `src/config.py` or `.env`:
```env
DB_HOST=<RDS-ENDPOINT>
DB_USER=admin
DB_PASSWORD=<your-rds-password>
DB_NAME=healthcare_db
```

---

## 🔄 Step 4: Automated Pipeline (Optional)

### Using Cron Job
```bash
# Edit crontab
crontab -e

# Run pipeline daily at 2 AM
0 2 * * * cd /home/ec2-user/healthcare-data-platform && python3 -m src.main >> /var/log/healthcare_etl.log 2>&1
```

### Using AWS Lambda (Serverless)
For smaller datasets, you can package the validation and ingestion logic as a Lambda function triggered by S3 events.

---

## 📊 Step 5: Power BI Connection

### Option A: Connect to RDS MySQL
1. Open Power BI Desktop
2. Get Data → MySQL Database
3. Server: `<RDS-ENDPOINT>`
4. Database: `healthcare_db`
5. Enter credentials

### Option B: Connect to S3
1. Open Power BI Desktop
2. Get Data → Amazon S3
3. Enter S3 bucket name
4. Select processed CSV files

---

## 🏗 Architecture on AWS

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│  S3 Bucket  │────▶│  EC2 Instance │────▶│  RDS (MySQL)   │
│  (Raw Data) │     │  (ETL/Spark)  │     │  (OLTP Store)  │
└─────────────┘     └──────────────┘     └────────────────┘
                           │
                           ▼
                    ┌──────────────┐     ┌────────────────┐
                    │  S3 Bucket   │────▶│   Power BI     │
                    │  (Processed) │     │  (Dashboard)   │
                    └──────────────┘     └────────────────┘
```

---

## 💰 Cost Estimation (Monthly)

| Service | Tier | Approx. Cost |
|---------|------|--------------|
| EC2 (t2.medium) | On-demand | ~$34/month |
| RDS (db.t3.micro) | Free tier | $0 (1st year) |
| S3 | Standard | ~$1-5/month |
| **Total** | | **~$35-40/month** |

> 💡 Use **Free Tier** instances for development/testing.

---

## ✅ Deployment Checklist

- [ ] S3 bucket created and data uploaded
- [ ] EC2 instance launched with dependencies
- [ ] RDS MySQL instance running with schema
- [ ] Config updated with RDS endpoint
- [ ] Pipeline tested on EC2
- [ ] Power BI connected to RDS/S3
- [ ] Cron job configured (optional)
