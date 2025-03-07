/* 自定义 JavaScript */

document.addEventListener('DOMContentLoaded', function() {
  // 添加图表响应式调整
  const resizeCharts = function() {
    const charts = document.querySelectorAll('.chart-container');
    if (charts.length > 0) {
      charts.forEach(function(chart) {
        if (typeof chart.resize === 'function') {
          chart.resize();
        }
      });
    }
  };

  // 监听窗口大小变化
  window.addEventListener('resize', resizeCharts);
  
  // 添加表格排序功能
  const tables = document.querySelectorAll('.md-typeset table:not([class])');
  if (tables.length > 0) {
    tables.forEach(function(table) {
      makeTableSortable(table);
    });
  }
  
  // 添加回到顶部按钮
  addBackToTopButton();
});

// 表格排序功能
function makeTableSortable(table) {
  const headers = table.querySelectorAll('th');
  headers.forEach(function(header, index) {
    header.addEventListener('click', function() {
      sortTable(table, index);
    });
    header.style.cursor = 'pointer';
    header.title = '点击排序';
  });
}

function sortTable(table, columnIndex) {
  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  const direction = table.getAttribute('data-sort-direction') === 'asc' ? -1 : 1;
  
  // 排序行
  rows.sort(function(rowA, rowB) {
    const cellA = rowA.querySelectorAll('td')[columnIndex].textContent.trim();
    const cellB = rowB.querySelectorAll('td')[columnIndex].textContent.trim();
    
    // 尝试数字排序
    const numA = parseFloat(cellA);
    const numB = parseFloat(cellB);
    
    if (!isNaN(numA) && !isNaN(numB)) {
      return direction * (numA - numB);
    }
    
    // 字符串排序
    return direction * cellA.localeCompare(cellB, 'zh-CN');
  });
  
  // 更新表格
  rows.forEach(function(row) {
    tbody.appendChild(row);
  });
  
  // 切换排序方向
  table.setAttribute('data-sort-direction', direction === 1 ? 'asc' : 'desc');
}

// 添加回到顶部按钮
function addBackToTopButton() {
  const button = document.createElement('button');
  button.innerHTML = '↑';
  button.className = 'back-to-top';
  button.title = '回到顶部';
  button.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: var(--md-primary-fg-color);
    color: white;
    border: none;
    font-size: 20px;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.3s;
    z-index: 100;
  `;
  
  document.body.appendChild(button);
  
  button.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  
  window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
      button.style.opacity = '1';
    } else {
      button.style.opacity = '0';
    }
  });
} 