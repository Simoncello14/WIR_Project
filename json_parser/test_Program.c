#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <string.h>
#include "cJSON/cJSON.c"

#define SEEDS_SIZE 42
#define STRINGS_SIZE 50

int actual_num_domains = 0; //the real number of domains. Initialized to 0.
struct invertedIndexStructure
{ 
   char* domain; 
   char** users; 
   int users_size; //lenght of the array of users.
};
typedef struct invertedIndexStructure invertedIndexEntry; /*This structure will be our inverted index of domains and users 
who shared posts about these domains.*/

int is_in(char* item, char** array, int lenght) {
    for (int i = 0; i < lenght; ++i) 
        if (!strcmp(array[i], item)) {
            //printf("\n\nFINO A QUI NUN CE PIOVE!!\n\n");
            return 1;
        }
    return 0;
}

char** seedArray(const char* const seeds, int num_seeds) {
    const cJSON *first_Domain = NULL;
    cJSON *seeds_json = cJSON_Parse(seeds);
    //Errors handling
    if (seeds_json == NULL)
    {
        const char *error_ptr = cJSON_GetErrorPtr();
        if (error_ptr != NULL)
        {
            fprintf(stderr, "Error before: %s\n", error_ptr);
        }
        goto end;
    }


    first_Domain = seeds_json -> child;

    //printf("%s\n", first_Domain->valuestring);


    cJSON *domains_Iterator = first_Domain;
    int domains_size = num_seeds;
    char** arr = (char**) malloc(num_seeds * sizeof(char*));

    int i = 0;
    while (domains_Iterator != NULL) {
        arr[i] = (char*) malloc(STRINGS_SIZE*sizeof(char));
        strcpy(arr[i],domains_Iterator -> valuestring);
        //printf("%s\n", arr[i]);
        //if (i != 0) printf("%s\n", a[i - 1]);
        //arr[i] = domains_Iterator ->valuestring;
        ++i;
        domains_Iterator = domains_Iterator -> next;
    }

    end:
    cJSON_Delete(seeds_json);

    //printf("%s\n", a[0]);
    return arr;
}


invertedIndexEntry* parsing(const char * const domains, int num_domains, int num_min_users)
{
    const cJSON *first_Domain = NULL;
    cJSON *domains_json = cJSON_Parse(domains);
    invertedIndexEntry* inv_index = NULL;

    //Errors handling
    if (domains_json == NULL)
    {
        const char *error_ptr = cJSON_GetErrorPtr();
        if (error_ptr != NULL)
        {
            fprintf(stderr, "Error before: %s\n", error_ptr);
        }
        goto end;
    }
    //--------------



    first_Domain = domains_json -> child;


    cJSON *domains_Iterator = first_Domain;
    int domains_size = num_domains;
    inv_index = malloc(domains_size * sizeof(invertedIndexEntry));
    int inv_index_i = 0;
    int users_size;

    while (domains_Iterator != NULL) {
        //printf("%s\n", name->string);
        users_size = num_min_users;
        inv_index[inv_index_i].domain = (char*) malloc(STRINGS_SIZE*sizeof(char));
        strcpy(inv_index[inv_index_i].domain, domains_Iterator -> string);
        //inv_index[inv_index_i].domain = domains_Iterator -> string;
        const cJSON *users_Iterator = domains_Iterator -> child;
        inv_index[inv_index_i].users = (char **) malloc(users_size*sizeof(char*));
        int i = 0;
        while (users_Iterator != NULL) {
                inv_index[inv_index_i].users[i] = (char*) malloc(STRINGS_SIZE*sizeof(char));
                strcpy(inv_index[inv_index_i].users[i], users_Iterator -> valuestring);
                //inv_index[inv_index_i] = users_Iterator -> valuestring;
                ++i;
                //printf("\n\nFIno a qui ce stamo\n\n\n");
                if (i == users_size) {
                    //i have to allocate a larger portion of memory.
                    //printf("\n\n\n\n\n\n\nDAJE CO STA REALLOCC!!!!!\n\n\n\n\n\n");
                    users_size = users_size * 2;
                    char** ptr = realloc(inv_index[inv_index_i].users, users_size * sizeof(char*));
                    //printf("\n\nRealloc!\n\n");
                    if (ptr == NULL)  {       // reallocated pointer ptr1 
                        printf("Exiting!!\n");
                        free(ptr);
                        exit(0);
                    }
                    else {
                        inv_index[inv_index_i].users = (char**) ptr;           // the reallocation succeeded, we can overwrite our original pointer now
                        //printf("\n\n\n\n\n\nDAJE CAZZO\n\n\n\n\n\n");
                    }
                }
                users_Iterator = users_Iterator -> next;
        }

        //printf("\n\nFINO A QUI NUN CE PIOVE!!\n\n");
        inv_index[inv_index_i].users_size = i;

        ++inv_index_i;
        actual_num_domains = inv_index_i;
        //if (inv_index_i == num_domains) printf("VAFFANCULO%d\n",inv_index_i);
        
        domains_Iterator = domains_Iterator -> next;
    }




end:
    cJSON_Delete(domains_json);
    return inv_index;
}


invertedIndexEntry get_posting(invertedIndexEntry* inv_index, char* domain) {
    for (int i = 0; i < actual_num_domains; ++i) {
        if (!strcmp(inv_index[i].domain, domain)) {
            return inv_index[i];
        }
    }
    //printf("\n\nFINO A QUI NUN CE PIOVE!!\n\n");
    //return NULL;
}

int and_score(invertedIndexEntry posting1, invertedIndexEntry posting2) {
    int size = posting1.users_size > posting2.users_size ? posting1.users_size : posting2.users_size;

    int score = 0;

    for(int i = 0; i < posting1.users_size; ++i) {
        for (int j = 0; j < posting2.users_size; ++j)
        {
            if (!strcmp(posting1.users[i], posting2.users[j])) ++score;
        }
    }

    return score;
}

int bias_calculator(invertedIndexEntry* inv_index, char** seed_domains, char* domain) {
    int bias = 0;
    invertedIndexEntry domain_posting = get_posting(inv_index, domain); //posting of the domain we are calculating the bias
    for (int i = 0; i < actual_num_domains; ++i) {
        if (is_in(inv_index[i].domain, seed_domains, SEEDS_SIZE)) {
            int similarity = and_score(domain_posting, inv_index[i]);
            //printf("\n\n\n\n\n%d\n\n\n\n\n", similarity );
            if (similarity > bias) {
                bias = similarity;
                //printf("\n\nFINO A QUI NUN CE PIOVE!!\n\n");
            }
        }
        //if ((i % 100) == 0) printf("\n\n\n\n\n\n\n%d\n\n\n\n\\n", i);
    }
    //printf("\n\nFINO A QUI NUN CE PIOVE!! BIAS = %d\n\n",bias);
    return bias;
}

int max_bias(invertedIndexEntry* inv_index, char** seed_domains) {
    int max = 0;
    for (int i = 0; i < actual_num_domains; ++i)
    {
        int score = bias_calculator(inv_index, seed_domains, inv_index[i].domain);
        if (score > max) max = score;
        //printf("%d\n", score);
    }
    printf("DAJEEEE\n");
    return max;
}


int main(int argc, char** argv)
{
        char* filename;
        char* fileseed;
        FILE *fp;
        struct stat filestatus;
        int file_size;
        char* file_contents;
        int num_domains;
        int num_min_users;

        if (argc != 5) {
                fprintf(stderr, "%s Usage: <file_json> <domains number> <minimal number of users per domain> <fileseed> <m\n", argv[0]);
                return 1;
        }

        filename = argv[1];
        fileseed = argv[4];
        //printf("%s\n", argv[4]);
        num_domains = atoi(argv[2]);
        num_min_users = atoi(argv[3]);
        //printf("%d\n", num_domains);
        //printf("%d\n", num_min_users);

        if ( stat(filename, &filestatus) != 0) {
                fprintf(stderr, "File %s not found\n", filename);
                return 1;
        }
        file_size = filestatus.st_size;


        file_contents = (char*) malloc(filestatus.st_size);

        if ( file_contents == NULL) {
                fprintf(stderr, "Memory error: unable to allocate %d bytes\n", file_size);
                return 1;
        }

        fp = fopen(filename, "rt");
        if (fp == NULL) {
                fprintf(stderr, "Unable to open %s\n", filename);
                fclose(fp);
                free(file_contents);
                return 1;
        }
        if ( fread(file_contents, file_size, 1, fp) != 1 ) {
                fprintf(stderr, "Unable t read content of %s\n", filename);
                fclose(fp);
                free(file_contents);
                return 1;
        }
        fclose(fp);



        if ( stat(fileseed, &filestatus) != 0) {
                fprintf(stderr, "File %s not found\n", fileseed);
                return 1;
        }
        file_size = filestatus.st_size;


        char* file_seed_contents = (char*) malloc(filestatus.st_size);

        if ( file_seed_contents == NULL) {
                fprintf(stderr, "Memory error: unable to allocate %d bytes\n", file_size);
                return 1;
        }

        fp = fopen(fileseed, "rt");
        if (fp == NULL) {
                fprintf(stderr, "Unable to open %s\n", fileseed);
                fclose(fp);
                free(file_seed_contents);
                return 1;
        }
        if ( fread(file_seed_contents, file_size, 1, fp) != 1 ) {
                fprintf(stderr, "Unable t read content of %s\n", fileseed);
                fclose(fp);
                free(file_seed_contents);
                return 1;
        }
        fclose(fp);
        

        //printf("%s\n", file_contents);

        printf("--------------------------------\n\n\n\n\n\n\n\n");


        //PARSING
        invertedIndexEntry* inv_index = parsing(file_contents, num_domains, num_min_users);
        //Filling array seed domains
        char** arr = (char**) seedArray(file_seed_contents, SEEDS_SIZE);
        printf("DAJE CAZZO PROVAMOCE %d\n",actual_num_domains);
        /*for (int i = 0; i <  42; ++i) {
            printf("%s\n", arr[i]);
        }
        printf("%s\n", arr[4]);
        */
        //printf("\n\nFINO A QUI NUN CE PIOVE!!\n\n");
        int bias;
        bias = bias_calculator(inv_index, arr, "www.alternet.org");
        //printf("DAJEEEE\n");
        int maxbias = max_bias(inv_index, arr);
//printf("DAJEEEE\n");
        //printf("osjkdhfg, %s\n", inv_index[1].domain);
        float f = (float) bias / (float) maxbias;
        printf("\n\n\nTi prego funziona %f\n", f);
        return 0;
}
