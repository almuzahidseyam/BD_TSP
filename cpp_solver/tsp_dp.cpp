#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>

using namespace std;

const double INF = 1e9;

int main() {
    int n;
    if (!(cin >> n)) return 0;

    vector<vector<double>> dist(n, vector<double>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> dist[i][j];
        }
    }

    // dp[mask][last_node] stores the minimum travel distance
    int num_masks = 1 << n;
    vector<vector<double>> dp(num_masks, vector<double>(n, INF));
    vector<vector<int>> parent(num_masks, vector<int>(n, -1));

    // Base case: Start at node 0 (Dhaka / Logistics HQ)
    dp[1][0] = 0.0;

    for (int mask = 1; mask < num_masks; ++mask) {
        for (int u = 0; u < n; ++u) {
            if (!(mask & (1 << u))) continue; // u must be in the visited set
            if (dp[mask][u] >= INF) continue;

            for (int v = 0; v < n; ++v) {
                if (mask & (1 << v)) continue; // v is already visited
                
                int next_mask = mask | (1 << v);
                double new_cost = dp[mask][u] + dist[u][v];
                if (new_cost < dp[next_mask][v]) {
                    dp[next_mask][v] = new_cost;
                    parent[next_mask][v] = u;
                }
            }
        }
    }

    // Find the minimum cost to return to 0 (Complete the delivery loop)
    double min_cost = INF;
    int last_node = -1;
    int full_mask = num_masks - 1;

    for (int i = 1; i < n; ++i) {
        double cost = dp[full_mask][i] + dist[i][0];
        if (cost < min_cost) {
            min_cost = cost;
            last_node = i;
        }
    }

    // Reconstruct path
    vector<int> path;
    int curr_mask = full_mask;
    int curr_node = last_node;

    while (curr_node != -1) {
        path.push_back(curr_node);
        int p = parent[curr_mask][curr_node];
        curr_mask ^= (1 << curr_node);
        curr_node = p;
    }

    cout << fixed << setprecision(2) << min_cost << endl;
    for (int i = path.size() - 1; i >= 0; --i) {
        cout << path[i] << " ";
    }
    cout << 0 << endl; // Return to HQ

    return 0;
}
