#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include "cJSON/cJSON.c"


struct invertedIndexStructure
{ 
   char* domain; 
   char** users; 
};
typedef struct invertedIndexStructure invertedIndex;


int parsing(const char * const domains)
{
    const cJSON *resolution = NULL;
    const cJSON *resolutions = NULL;
    const cJSON *name = NULL;
    int status = 0;
    cJSON *domains_json = cJSON_Parse(domains);
    if (domains_json == NULL)
    {
        const char *error_ptr = cJSON_GetErrorPtr();
        if (error_ptr != NULL)
        {
            fprintf(stderr, "Error before: %s\n", error_ptr);
        }
        status = 0;
        goto end;
    }

    name = cJSON_GetObjectItemCaseSensitive(domains_json, "www.oyejuanjo.com");
    //nt finiti = FALSE;
    invertedIndex* inv_index = malloc(3000000 * sizeof(invertedIndex));
    int indice = 0;
    while (name != NULL) {
        //printf("%s\n", name->string);
        inv_index[indice].domain = name -> string;
        inv_index[indice].users = (char **) malloc(40*sizeof(char*));
        int i = 0;
        const cJSON *iterator = name -> child;
        while (iterator != NULL) {
                inv_index[indice].users[i] = (iterator) -> valuestring;
                iterator = iterator -> next;
                ++i;
        }
        ++indice;
        name = name -> next;
     }

     printf("\n\n%d\n\n", indice);



     //Voglio stampare l'array di struct che ho creato

      for (int i=0; i < indice - 1; ++i) {
        printf("%s: ",inv_index[i].domain);
        for (int j = 0; j < 1; ++j) {
                printf("%s: ",inv_index[i].users[j]);
        }
     }

end:
    cJSON_Delete(domains_json);
    return status;
}


int main(int argc, char** argv)
{
        char* filename;
        FILE *fp;
        struct stat filestatus;
        int file_size;
        char* file_contents;

        if (argc != 2) {
                fprintf(stderr, "%s <file_json>\n", argv[0]);
                return 1;
        }
        filename = argv[1];

        if ( stat(filename, &filestatus) != 0) {
                fprintf(stderr, "File %s not found\n", filename);
                return 1;
        }
        file_size = filestatus.st_size;
        file_contents = (char*)malloc(filestatus.st_size);
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

        //printf("%s\n", file_contents);

        printf("--------------------------------\n\n\n\n\n\n\n\n");

        parsing(file_contents);
        printf("\n\n\n");
        return 0;
}
