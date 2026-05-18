# 使用官方 Python 映像檔作為基礎
FROM python:3.11-slim-bookworm

# 設定工作目錄
WORKDIR /app

# 安裝 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 複製專案設定檔
COPY pyproject.toml uv.lock ./

# 安裝依賴 (不包含專案本身)
RUN uv sync --frozen --no-install-project

# 複製專案原始碼
COPY . .

# 安裝專案
RUN uv sync --frozen

# 設定環境變數
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# 執行指令
CMD ["uv", "run", "main.py"]
