const API_BASE = "http://127.0.0.1:8000"; // 같은 오리진이면 "" 유지, 별도 포트/도메인이면 예: "http://127.0.0.1:8000"

const state = {
    page: 1,
    size: 10,
    totalPages: 1,
    total: 0,
    category: "",
    q: "",
};

const categoryFilter = document.getElementById("categoryFilter");
const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");
const noticeTbody = document.getElementById("noticeTbody");
const paginationEl = document.getElementById("pagination");

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&")
        .replaceAll("<", "<")
        .replaceAll(">", ">")
        .replaceAll('"', '"')
        .replaceAll("'", "'");
}

function formatDate(isoStr) {
    if (!isoStr) return "-";
    const d = new Date(isoStr);
    if (Number.isNaN(d.getTime())) return isoStr;
    return d.toLocaleDateString("ko-KR");
}

async function loadNoticeList(targetPage = state.page) {
    state.page = targetPage;

    const params = new URLSearchParams({
        page: String(state.page),
        size: String(state.size),
    });

    if (state.category && state.category !== "전체" && state.category !== "all") {
        params.set("category", state.category);
    }
    if (state.q) {
        params.set("q", state.q);
    }

    try {
        const res = await fetch(`${API_BASE}/api/notices?${params.toString()}`);
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }

        const data = await res.json();
        console.log("공지사항 데이터:", data);
        const items = Array.isArray(data) ? data : (data.items ?? []);
        state.total = data.total ?? items.length;
        state.page = data.page ?? state.page;
        state.totalPages = data.totalPages ?? 1;

        renderTable(items);
        renderPagination();
    } catch (err) {
        console.error("공지사항 불러오기 실패:", err);
        if (noticeTbody) {
            noticeTbody.innerHTML = `
        <tr>
          <td colspan="5">공지사항을 불러오는 중 오류가 발생했습니다.</td>
        </tr>
      `;
        }
    }
}

async function requestNotice(url, options = {}) {
    const fullUrl = url.startsWith("http")
        ? url
        : `${API_BASE}${url.startsWith("/") ? "" : "/"}${url}`;

    const config = {
        ...options,
        headers: {
            ...(options.body ? { "Content-Type": "application/json" } : {}),
            ...(options.headers || {}),
        },
    };

    const res = await fetch(fullUrl, config);
    const contentType = res.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
        ? await res.json()
        : await res.text();

    if (!res.ok) {
        const message =
            (typeof data === "object" && data && (data.detail || data.message)) ||
            `요청 실패 (HTTP ${res.status})`;
        throw new Error(message);
    }

    return data;
}

function renderTable(notices) {
    if (!noticeTbody) return;

    if (!notices.length) {
        noticeTbody.innerHTML = `
      <tr>
        <td colspan="5">등록된 공지사항이 없습니다.</td>
      </tr>
    `;
        return;
    }

    noticeTbody.innerHTML = notices
        .map((notice) => {
            const pinBadge = notice.isPinned ? "[고정] " : "";
            const detailUrl = `./notice-detail.html?id=${encodeURIComponent(notice.id)}`;
            return `
      <tr>
          <td align="center">${escapeHtml(notice.category || "일반")}</td>
          <td>
            <a href="${detailUrl}">${pinBadge}${escapeHtml(notice.title)}</a>
          </td>
          <td align="center">${escapeHtml(notice.author || "관리자")}</td>
          <td align="center">${Number(notice.views ?? 0)}</td>
          <td align="center">${escapeHtml(formatDate(notice.createdAt))}</td>
        </tr>
      `;
        })
        .join("");
}

function renderPagination() {
    if (!paginationEl) return;

    if (state.totalPages <= 1) {
        paginationEl.innerHTML = "";
        return;
    }

    const buttons = [];

    buttons.push(`
    <button type="button" data-page="${state.page - 1}" ${state.page <= 1 ? "disabled" : ""}>
      이전
    </button>
  `);

    for (let p = 1; p <= state.totalPages; p += 1) {
        const activeAttr = p === state.page ? 'aria-current="page" class="active"' : "";
        buttons.push(`
      <button type="button" data-page="${p}" ${activeAttr}>
        ${p}
      </button>
    `);
    }

    buttons.push(`
    <button type="button" data-page="${state.page + 1}" ${state.page >= state.totalPages ? "disabled" : ""}>
      다음
    </button>
  `);

    paginationEl.innerHTML = buttons.join("");
}

if (categoryFilter) {
    categoryFilter.addEventListener("change", (e) => {
        state.category = e.target.value;
        loadNoticeList(1);
    });
}

function triggerSearch() {
    state.q = searchInput ? searchInput.value.trim() : "";
    loadNoticeList(1);
}

if (searchBtn) {
    searchBtn.addEventListener("click", triggerSearch);
}

if (searchInput) {
    searchInput.addEventListener("keyup", (e) => {
        if (e.key === "Enter") {
            triggerSearch();
        }
    });
}

if (paginationEl) {
    paginationEl.addEventListener("click", (e) => {
        const btn = e.target.closest("button[data-page]");
        if (!btn || btn.disabled) return;
        const nextPage = Number(btn.dataset.page);
        if (Number.isInteger(nextPage) && nextPage >= 1 && nextPage <= state.totalPages) {
            loadNoticeList(nextPage);
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadNoticeList(1);
});