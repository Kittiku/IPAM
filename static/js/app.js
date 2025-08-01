// static/js/app.js

/**
 * แสดง Toast Notification บนหน้าจอ
 * @param {string} message ข้อความที่ต้องการแสดง
 * @param {'info' | 'success' | 'error'} type ประเภทของ notification
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) {
        console.error('Toast container not found!');
        return;
    }

    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    
    const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        info: 'bg-blue-500'
    };

    const toast = document.createElement('div');
    toast.className = `flex items-center text-white px-6 py-4 rounded-md shadow-lg transform transition-all duration-300 translate-y-4 opacity-0 ${colors[type]}`;
    toast.innerHTML = `
        <i class="fas ${icons[type]} mr-3 text-xl"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);
    
    // Animate in
    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-4', 'opacity-0');
    });

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        toast.classList.add('opacity-0');
        toast.addEventListener('transitionend', () => toast.remove());
    }, 5000);
}

// เพิ่ม CSS ที่จำเป็นสำหรับ components บางตัวเข้าไปใน style.css
// หรือจะใส่ใน <style> block ของ HTML ก็ได้
const sharedStyles = `
    .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .card-hover { transition: all 0.3s ease; }
    .card-hover:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04); }
    .loading-spinner { animation: spin 1s linear infinite; }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .status-indicator { animation: pulse 2s infinite; }
    .tab-button { padding: 0.75rem 1.5rem; border-bottom: 3px solid transparent; cursor: pointer; transition: all 0.3s ease; font-weight: 500; color: #6b7280; }
    .tab-button.active { border-bottom-color: #6366f1; color: #6366f1; background-color: #f9fafb; }
    .tab-content { display: none; }
    .tab-content.active { display: block; animation: fadeIn 0.5s; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
`;

// สร้าง element <style> แล้วใส่เข้าไปใน head
const styleSheet = document.createElement("style");
styleSheet.innerText = sharedStyles;
document.head.appendChild(styleSheet);