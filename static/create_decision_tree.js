/**
 * Function to create a decision tree visualization using D3.js
 * @param {Array} data - The decision tree data
 */
function createDecisionTree(data) {
    d3.select("svg").selectAll("*").remove();
    // Prepare the tree data structure
    const treeData = {
        name: data[0].question + " (" + (data[0].yes.length + data[0].no.length) + ")" + " (" + data[0].information_gain.toFixed(3) + ")",
        children: [
            {
                name: 'yes (' + data[0].yes.length + ')',
                children: buildTree(data, data[0].yes, 1)
            },
            {
                name: 'no (' + data[0].no.length + ')',
                children: buildTree(data, data[0].no, 1)
            }
        ]
    };

    /**
     * Recursive function to build the tree structure
     * @param {Array} data - The decision tree data
     * @param {Array} names - The names of the characters
     * @param {number} index - The current index in the data array
     * @returns {Array} - The tree structure
     */
    function buildTree(data, names, index) {
        if (index >= data.length || names.length === 0) {
            return names.map(name => ({ name: name + ' (1)' }));
        }
        const question = data[index];
        const yesNames = names.filter(name => question.yes.includes(name));
        const noNames = names.filter(name => question.no.includes(name)); 
        return [
            {
                name: question.question + " (" + names.length + ")" + question.information_gain.toFixed(3),
                children: [
                    {
                        name: 'yes (' + yesNames.length + ')',
                        children: buildTree(data, yesNames, index + 1)
                    },
                    {
                        name: 'no (' + noNames.length + ')',
                        children: buildTree(data, noNames, index + 1)
                    }
                ]
            }
        ];
    }

    // Set up the SVG canvas
    const svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height"),
        g = svg.append("g").attr("transform", "translate(40,40)");

    // Create a D3 tree layout
    const tree = d3.tree().size([width - 160, height - 160]);
    const root = d3.hierarchy(treeData);

    tree(root);

    // Draw the links (edges) between nodes
    const link = g.selectAll(".link")
        .data(root.descendants().slice(1))
        .enter().append("path")
        .attr("class", "link")
        .attr("d", d => `
            M${d.x},${d.y}
            C${d.x},${(d.y + d.parent.y) / 2}
             ${d.parent.x},${(d.y + d.parent.y) / 2}
             ${d.parent.x},${d.parent.y}
        `)
        .style("fill", "none")
        .style("stroke", "#ccc")
        .style("stroke-width", "2px");

    // Draw the nodes
    const node = g.selectAll(".node")
        .data(root.descendants())
        .enter().append("g")
        .attr("class", d => "node" + (d.children ? " node--internal" : " node--leaf"))
        .attr("transform", d => `translate(${d.x},${d.y})`);

    // Append circles to the nodes
    node.append("circle")
        .attr("r", 5);

    // Append text labels to the nodes
    node.append("text")
        .attr("dy", 3)
        .attr("x", d => d.children ? 10 : 10)  // Position to the right for all nodes
        .attr("transform", d => d.children ? "" : "rotate(90)")  // Rotate only the names
        .style("text-anchor", "start")  // Align all text to the right
        .text(d => d.data.name);
}
