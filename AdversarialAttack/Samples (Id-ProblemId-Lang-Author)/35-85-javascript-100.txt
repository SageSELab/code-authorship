function maximalRectangle(aa) {
    let m = aa.length,
        n = aa[0].length;

    let heights = new Array(n + 1).fill(0), // this row heights, last col is 0
        maxArea = 0;

    for (let r = 0; r < m; r++) {
        let cols = []; // prev increasing columns - stack
        cols.top = () => cols[cols.length - 1]; // get column left on top of stack

        for (let c = 0; c <= n; c++) {
            if (c < n) {
                if (aa[r][c] === "1") heights[c]++;
                else heights[c] = 0;
            }

            while (cols.length && heights[cols.top()] > heights[c]) {
                let height = heights[cols.pop()]; // prev column height
                let width = cols.length ? c - cols.top() - 1 : c; // prev prev column to cur column width
                maxArea = Math.max(maxArea, width * height);
            }
            cols.push(c);
        }
    }
    return maxArea;
}