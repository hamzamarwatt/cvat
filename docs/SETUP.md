# Setup (assessment submission)

## Prerequisites

- Docker with Compose plugin, ~8 GB RAM, ~15 GB disk
- Public GitHub **fork** of https://github.com/cvat-ai/cvat (do not PR upstream)

## Run CVAT with local changes

```bash
export CVAT_HOST=localhost
cd cvat
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
```

Open http://localhost:8080

## COCO sample data

```bash
wget http://images.cocodataset.org/zips/val2017.zip
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
unzip -q val2017.zip && unzip -q annotations_trainval2017.zip
```

Create a task, upload a subset of `val2017/` images, then **Actions → Upload annotations → COCO 1.0** with `annotations/instances_val2017.json`.

## Git remotes

```bash
git remote rename origin upstream   # if cloned from cvat-ai
git remote add origin https://github.com/<your-user>/cvat.git
git push -u origin dev-test01
```

Open PR: `dev-test01` → `main` on **your fork**.

## Class analytics page

http://localhost:8080/tasks/<task_id>/class-analytics
