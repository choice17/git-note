#include <vector>
#include <iostream>
#include <utility>

using namespace std;

using Graph = vector<vector< int>>;
using bGraph = vector<vector< bool>>;

void init_graph(Graph &graph, int rows, int cols)
{
    graph.resize(rows);
    int val = 0;
    for (int i = 0; i < rows; ++i) {
        graph[i].resize(cols);
        vector<int>& row = graph[i];
        for (int j = 0; j < cols; ++j) {
            row[j] = val++;
        }
    }
}
void init_bGraph(bGraph &graph, int rows, int cols)
{
    graph.resize(rows);
    for (int i = 0; i < rows; ++i) {
        graph[i].resize(cols);
    }
}

void tranversebfs(const Graph &graph, int sx, int sy, int ex, int ey)
{
    bGraph visited;
    int h = graph.size(), w = graph[0].size();
    init_bGraph(visited, h, w);
    
    vector<int > queue;
    int gsize = h * w;
    static const vector<pair<int,int> > steps = {{0,1},{1,0},{0,-1},{-1,0}};

    queue.push_back((sx << 16) + sy);
    //for (;;) {
        //vector<int> tqueue;
        while (queue.size()) {
            int val = queue.front();
            queue.erase(queue.begin());
            int sx = val >> 16, sy = val & 0xffff;
            if (visited[sy][sx])
                continue;
            visited[sy][sx] = true;
            cout << graph[sy][sx] << ",";
            if (sx == ex && sy == ey) {
                cout << "reach dest!\n";
                return;
            }
            for (const auto& step : steps) {
                int ssx = sx + step.first, ssy = sy + step.second;
                if ((ssx < 0) || (ssx >= w) || (ssy < 0) || (ssy >= h))
                    continue;
                if (visited[ssy][ssx])
                    continue;
                queue.push_back((ssx << 16) + ssy); 
                //tqueue.push_back((ssx << 16) + ssy); 
            }
        }
        //swap(queue,tqueue);
    //}
}

void tranversedfs(const Graph &graph, int sx, int sy, int ex, int ey)
{
    bGraph visited;
    int h = graph.size(), w = graph[0].size();
    init_bGraph(visited, h, w);
    
    vector<int > stack;
    int gsize = h * w;
    static const vector<pair<int,int> > steps = {{0,1},{1,0},{0,-1},{-1,0}};

    stack.push_back((sx << 16) + sy);

    while (stack.size()) {
        int val = stack.back();
        stack.pop_back();
        int sx = val >> 16, sy = val & 0xffff;
        if (visited[sy][sx])
            continue;
        visited[sy][sx] = true;
        cout << graph[sy][sx] << ",";
        if (sx == ex && sy == ey) {
            cout << "reach dest!\n";
            return;
        }
        for (const auto& step : steps) {
            int ssx = sx + step.first, ssy = sy + step.second;
            if ((ssx < 0) || (ssx >= w) || (ssy < 0) || (ssy >= h))
                continue;
            if (visited[ssy][ssx])
                continue;
            stack.push_back((ssx << 16) + ssy); 
        }
    }

}

void print_graph(const Graph& g)
{
    int h = g.size(), w = g[0].size();
    for (int i = -1; i < w; i++) {
        printf("%3d ", i);
    } printf("\n");

    for (int i = 0; i < h; i++) {
        for (int j = -1; j < w; j++) {
            if (j == -1) printf("%3d ", i);
            else printf("%3d ", g[i][j]);
        } printf("\n");
    }
}
int main(int argc, char **argv)
{
    Graph graph;
    int h = 9, w = 9;
    int sx = 0, sy = 0, ex = 3, ey = 2; 
    if (argc == 7) {
        h = atoi(argv[1]);
        w = atoi(argv[2]);
        sx = atoi(argv[3]);
        sy = atoi(argv[4]);
        ex = atoi(argv[5]);
        ey = atoi(argv[6]);
    }
    init_graph(graph, h, w);
    printf("args: h:%d,w:%d (%d,%d)->(%d,%d)\n", h, w, sx, sy, ex, ey);
    print_graph(graph);
    cout << "tranverse bfs :\n";
    tranversebfs(graph, sx, sy, ex, ey);
    cout << "tranverse dfs :\n";
    tranversedfs(graph, sx, sy, ex, ey);
    return 0;
}

