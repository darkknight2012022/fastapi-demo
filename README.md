# FastAPI Trading Demo

一个完整的 FastAPI 后端服务示例，包含鉴权、测试、监控、CI/CD 全套工程实践。

## 技术栈
- **FastAPI** — 高性能 Python Web 框架
- **JWT** — 无状态鉴权
- **Prometheus + Grafana** — 监控可观测
- **Docker + Kubernetes** — 容器化部署
- **GitHub Actions** — CI/CD 流水线

## 快速启动
```bash
pip install fastapi uvicorn python-jose passlib python-multipart
uvicorn main:app --reload
```

## 接口文档
启动后访问 http://localhost:8000/docs

## 测试
```bash
pytest test_main.py -v      # 单元测试
pytest test_e2e.py -v -s    # E2E 测试
python3 -m locust -f locustfile.py --headless --users 10 --run-time 15s --host http://localhost:8000  # 压测
```

## CI/CD
每次 push 自动触发 GitHub Actions：代码检查 → 单元测试 → Docker 构建
