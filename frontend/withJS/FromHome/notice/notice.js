const API_BASE = "http://127.0.0.1:8000/api/notices";

async function requestNotice(url = API_BASE, options = {}) {
    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    if (!response.ok) {
        let message = `요청 실패 (${response.status})`;
        try {
            const err = await response.json();
            if (err.detail) message = err.detail;
        } catch (_) { }
        throw new Error(message);
    }

    return response.json();
}

function formatDate(isoString) {
    if (!isoString) return "-";
    const date = new Date(isoString);
    return date.toLocaleString("ko-KR", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
    });
}

function escapeHtml(str = "") {
    return String(str)
        .replaceAll("&", "&")
        .replaceAll("<", "<")
        .replaceAll(">", ">")
        .replaceAll('"', '"')
        .replaceAll("'", "'");
}