import numpy as np
import matplotlib.pyplot as plt
import random

def generate_tetrahedron_face_nodes(num_nodes=150):
    """
    Distributes `num_nodes` randomly across the 4 triangular faces of a tetrahedron
    and directly records their source face.
    """
    # 4 vertices of a tetrahedron
    vertices = np.array([
        [ 1.0,  1.0,  1.0],
        [ 1.0, -1.0, -1.0],
        [-1.0,  1.0, -1.0],
        [-1.0, -1.0,  1.0]
    ])

    # 4 faces, each defined by 3 vertex indices
    faces = [
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3)
    ]

    pos_3d = {}
    node_to_faces = {}

    for node_id in range(num_nodes):
        # 1. Pick a random face
        f_idx = random.randint(0, len(faces) - 1)
        vA, vB, vC = vertices[faces[f_idx][0]], vertices[faces[f_idx][1]], vertices[faces[f_idx][2]]

        # 2. Generate random barycentric coordinates for that triangle
        r1, r2 = random.random(), random.random()
        if r1 + r2 > 1:
            r1 = 1 - r1
            r2 = 1 - r2
        r3 = 1 - r1 - r2

        point = r1 * vA + r2 * vB + r3 * vC
        pos_3d[node_id] = point

        # 3. Directly assign the face index (no geometric checks needed!)
        node_to_faces[node_id] = [f_idx]

    return pos_3d, node_to_faces

def share_same_face(u, v, node_to_faces):
    """Checks if two nodes share at least one common face."""
    return len(set(node_to_faces[u]).intersection(set(node_to_faces[v]))) > 0

def sample_valid_edge_pairs(pos_3d, node_to_faces, num_matches):
    """Randomly samples pairs of vertices that share at least one face out of total match attempts."""
    node_ids = list(pos_3d.keys())
    valid_edges = []
    attempts = 0

    while attempts < num_matches:
        attempts += 1
        u, v = random.sample(node_ids, 2)
        edge = tuple(sorted((u, v)))

        if u == v:
            continue
        if edge in valid_edges:
            continue

        if share_same_face(u, v, node_to_faces):
            valid_edges.append(edge)

    return valid_edges

def export_puzzle_state(pos_3d, active_edge_pairs, output_filename="puzzle_step.png"):
    """
    Renders and exports the puzzle state purely through the active nodes and edges,
    allowing the 3D shape to emerge organically.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    visible_nodes = set()
    for u, v in active_edge_pairs:
        visible_nodes.add(u)
        visible_nodes.add(v)

    # 1. Render Visible Nodes
    if visible_nodes:
        node_list = list(visible_nodes)
        node_xyz = np.array([pos_3d[n] for n in node_list])
        ax.scatter(node_xyz[:, 0], node_xyz[:, 1], node_xyz[:, 2],
                   s=50, c='crimson', edgecolors='black', depthshade=True, zorder=3)

    # 2. Render Visible Puzzle Edges
    for u, v in active_edge_pairs:
        p1 = pos_3d[u]
        p2 = pos_3d[v]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                c='black', alpha=0.8, linewidth=2.0, zorder=2)

    # Clean up layout presentation
    ax.grid(False)
    ax.set_axis_off()

    # Enforce static spatial limits so camera framing stays completely steady
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])

    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Successfully saved snapshot to {output_filename}")

# 1. Initialize nodes distributed across the tetrahedron faces
num_players = 200
positions, node_faces = generate_tetrahedron_face_nodes(num_nodes=num_players)

# 2. Simulate playing a given number of matches
num_matches = 200
available_edges = sample_valid_edge_pairs(positions, node_faces, num_matches=num_matches)
print('After playing {} matches, players successfully found {} edges.'.format(
    num_matches, len(available_edges)))

# 3. Simulate gameplay stages based on the actual edges found
total_found = len(available_edges)

base_filename = "tetra_{}_{}".format(num_players, num_matches)

early_game = available_edges[:total_found // 8]
export_puzzle_state(positions, early_game, base_filename + "_early.png")

mid_game = available_edges[:total_found // 2]
export_puzzle_state(positions, mid_game, base_filename + "_mid.png")

late_game = available_edges
export_puzzle_state(positions, late_game, base_filename + "_late.png")
