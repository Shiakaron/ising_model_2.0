#include "header.h"

void initialise_system_and_maps() {
    N = (int)(pow(L,dim)+0.5);
    spins = new int[N];
    initialise_nearest_periodic();
    initialise_next2nearest_periodic();
}

void initialise_spins_cold() {
    int s = 2*(rand()%2)-1; //return -1 or 1 randomly (50/50)
    for (int i = 0; i<N; i++) {
        spins[i] = s; // initialise all to the value of s
    }
}

void initialise_spins_hot() {
    for (int i = 0; i<N; i++) {
        spins[i] = 2*(rand()%2)-1;    //return -1 or 1 randomly (50/50)
    }
}

void initialise_nearest_periodic() {
    // vector = [left, right, back, forw, down,up,.....]
    // initialise useful variables
    int temp;
    int addterm;
    int i_level;
    int temp_level;
    // begin identifying nearest neighbours
    for (int i=0; i<N; i++) {
        vector<int> nearests;
        for (int j=0; j<dim; j++) {
            addterm = (int)(pow(L,j+1)+0.5);
            i_level = i/(addterm);
            // left/back/down etc.
            temp = i - addterm/L;
            temp_level = floor((double)temp/(addterm));
            if (temp_level < i_level) temp += addterm;
            nearests.push_back(temp);
            // right/forw/up etc.
            temp = i + addterm/L;
            temp_level = floor((double)temp/(addterm));
            if (temp_level > i_level) temp -= addterm;
            nearests.push_back(temp);
        }
        // add vector to map
        mapOfNearest[i]=nearests;
    }
}

void initialise_next2nearest_periodic(){
    //vector = []
    // identify next-to-nearest neighbours
    int temp;
    //dim=1 is a special case
    if (dim == 1) {
        for (int i=0; i<N; i++) {
            vector<int> next2nearests;
            temp = i-2;
            if (temp < 0) temp += N;
            next2nearests.push_back(temp);
            temp = i+2;
            if (temp >= N) temp -= N;
            next2nearests.push_back(temp);
            // add vector to map
            mapOfNext2Nearest[i] = next2nearests;
        }
    }
    else {
        // initialise useful variables
        int temp2;
        int addtermJ;
        int addtermK;
        int i_level;
        int temp_level;
        int temp2_level;
        for (int i=0; i<N; i++) {
            vector<int> next2nearests;
            //dim>1
            for (int j=0; j<dim-1; j++) {
                addtermJ = (int)(pow(L,j+1)+0.5);
                i_level = i/(addtermJ);
                // small step first in positive direction
                temp = i + addtermJ/L;
                temp_level = floor((double)temp/(addtermJ));
                if (temp_level > i_level) temp -= addtermJ;
                // big steps
                for (int k=j+1; k<dim; k++) {
                    addtermK = (int)(pow(L,k+1)+0.5);
                    temp_level = temp/(addtermK);
                    // positive big step
                    temp2 = temp + addtermK/L;
                    temp2_level = floor((double)temp2/(addtermK));
                    if (temp2_level > temp_level) temp2 -= addtermK;
                    next2nearests.push_back(temp2);
                    // negative big step
                    temp2 = temp - addtermK/L;
                    temp2_level = floor((double)temp2/(addtermK));
                    if (temp2_level < temp_level) temp2 += addtermK;
                    next2nearests.push_back(temp2);
                }
                // small step in negative direction
                temp = i - addtermJ/L;
                temp_level = floor((double)temp/(addtermJ));
                if (temp_level < i_level) temp += addtermJ;
                // big steps
                for (int k=j+1; k<dim; k++) {
                    addtermK = (int)(pow(L,k+1)+0.5);
                    temp_level = temp/(addtermK);
                    // positive big step
                    temp2 = temp + addtermK/L;
                    temp2_level = floor((double)temp2/(addtermK));
                    if (temp2_level > temp_level) temp2 -= addtermK;
                    next2nearests.push_back(temp2);
                    // negative big step
                    temp2 = temp - addtermK/L;
                    temp2_level = floor((double)temp2/(addtermK));
                    if (temp2_level < temp_level) temp2 += addtermK;
                    next2nearests.push_back(temp2);
                }
            }
        // add vector to map
        mapOfNext2Nearest[i] = next2nearests;
        }
    }
}

void compute_magnetisation() {
    int m = 0;
    for(int i=0;i<N;i++){
            m += spins[i];
    }
    M = m;
}

double compute_denergy(int index) {
    vector<int> temp_vec;
    double de_nearest = 0;
    double de_next2nearest = 0;
    double de_externalfield = 0;

    //nearest neighbours
    temp_vec = mapOfNearest[index];
    for (int j = 0; j<temp_vec.size(); j++) {
        de_nearest += spins[temp_vec[j]];
    }
    de_nearest *= 2*spins[index];

    //next-to-nearest neighbours
    if (n2n!=0) {
        temp_vec = mapOfNext2Nearest[index];
        for (int j = 0; j<temp_vec.size(); j++) {
            de_next2nearest += spins[temp_vec[j]];
        }
        de_next2nearest *= 2*n2n*spins[index];
    }

    //external field
    if (H != 0) {
        de_externalfield += H*spins[index];
    }

    // return total change in energy
    int de_total = de_nearest + de_next2nearest + de_externalfield;
    return de_total;
}

void compute_energy() {
    double e_total = 0;
    int s_sum;
    int sum_nearest = 0;
    int sum_next2nearest = 0;
    vector<int> temp_vec;
    //cout << "compute_energy()\n";
    //nearest neightbours, J=1
    //cout << "nearests\n";
    for (int i=0; i<N; i++) {
        cout << i << ": ";
        //notice j+=2 to avoid double counting. For each index we consider left/back/down etc. directions
        temp_vec = mapOfNearest[i];
        s_sum = 0;
        for (int j = 0; j<temp_vec.size(); j+=2) {
            //cout << temp_vec[j] << " ";
            s_sum += spins[temp_vec[j]];
        }
        //cout << endl;
        sum_nearest += spins[i]*s_sum;
    }
    e_total -= sum_nearest;

    //nextonearest neighbours, J'=n2n
    if (n2n!=0) {
        //cout << "next2nearests\n";
        for (int i=0; i<N; i++) {
            //cout << i << ": ";
            temp_vec = mapOfNext2Nearest[i];
            s_sum = 0;
            for (int j = 0; j<temp_vec.size(); j+=2) {
                //cout << temp_vec[j] << " ";
                s_sum += spins[temp_vec[j]];
            }
            //cout << endl;
            sum_next2nearest += spins[i]*s_sum;
        }
        e_total -= n2n * sum_next2nearest;
    }

    //external field, mu = 1
    if (H!=0) {
        e_total += H*M;
    }
    E = e_total;
}

double average_energy() {
    // compute_energy first before calling this function
    double nearest_links = dim*N;
    double next2nearest_links = mapOfNext2Nearest[0].size(); // much faster and easier than the actual expression for the number of next to nearest links
    return E/(nearest_links+next2nearest_links*n2n);
}

void metropolis_function(double T, int cycles) {
    // initialise useful variables
    double de = 0;
    double beta = 1.0/T;
    double x;
    double flip_probability;
    int flips_counter = 0;
    int index;

    for(int r=0; r<cycles; r++){
        for(int k = 0; k<N; k++){
            //randomly select a site
            index = rand()%N;
            //measure energy difference before flip
            de = compute_denergy(index);
            //flip if the right condition is met
            if (de <= 0){
                spins[index] *= -1;
                flips_counter += spins[index];
            }
            else {
                x = ((double)rand()/RAND_MAX);
                flip_probability = exp(-beta*de);
                if (x < flip_probability) {
                    spins[index] *= -1;
                    flips_counter += spins[index];
                }
            }
        }
    }
    M += 2*flips_counter;
}
