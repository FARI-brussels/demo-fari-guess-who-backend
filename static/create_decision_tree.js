function createDecisionTree(data) {
    d3.select("svg").selectAll("*").remove();
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

    const svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height"),
        g = svg.append("g").attr("transform", "translate(40,40)");

    const tree = d3.tree().size([width - 160, height - 160]);
    const root = d3.hierarchy(treeData);

    tree(root);

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

    const node = g.selectAll(".node")
        .data(root.descendants())
        .enter().append("g")
        .attr("class", d => "node" + (d.children ? " node--internal" : " node--leaf"))
        .attr("transform", d => `translate(${d.x},${d.y})`);

    node.append("circle")
        .attr("r", 5);

    node.append("text")
        .attr("dy", 3)
        .attr("x", d => d.children ? 10 : 10)  // Position to the right for all nodes
        .attr("transform", d => d.children ? "" : "rotate(90)")  // Rotate only the names
        .style("text-anchor", "start")  // Align all text to the right
        .text(d => d.data.name);
}
