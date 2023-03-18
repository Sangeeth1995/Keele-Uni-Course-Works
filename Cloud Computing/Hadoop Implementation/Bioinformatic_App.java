// Importing libraries for mapreduce operation
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.MultipleOutputs;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
//import org.apache.hadoop.mapreduce.InputSplit;



public class Bioinformatic_App{
//  Creating TokenizerMapper function for performing Map operation
    public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable>{

        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            // Getting filepath using FileSplit librabry
            String filePathString = ((FileSplit) context.getInputSplit()).getPath().toString();   
            //Defining serach terms.In our case we used our Gene and its subterms            
            String Gene =   "GO:0030420";
            String subterm1 = "GO:0045808";
            String subterm2 = "GO:0045304";
            String subterm3 = "GO:0045809";
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                String temp = itr.nextToken();
                //Appemding filename path with the tokem
                String filepathword = filePathString + "*" + temp;
                //Performing a simple if operation to compare the token generated with our gene and child terms
                if (temp.compareTo(Gene) == 0){
                    word.set(filepathword);
                    context.write(word, one);
                }

                if (temp.compareTo(subterm1) == 0){
                    word.set(filepathword);
                    context.write(word, one);
                }
                if (temp.compareTo(subterm2) == 0){
                    word.set(filepathword);
                    context.write(word, one);
                }
                if (temp.compareTo(subterm3) == 0){
                    word.set(filepathword);
                    context.write(word, one);
                }
            } 
        }
    } 
 





    //Creating IntSumReducer function for Reducer operation
    public static class IntSumReducer extends Reducer<Text,IntWritable,Text,IntWritable> {

        Text one = new Text();
        private IntWritable result = new IntWritable();
        //We are using MultipleOutputs, since we are generating counts for mutiple input files
        private MultipleOutputs<Text,IntWritable> multipleoutputs;
        public void setup(Context context) throws IOException, InterruptedException {

            multipleoutputs = new MultipleOutputs<Text,IntWritable>(context);
        } 
        
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {

            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
        //Spliting key value pair of output we are recieving from Mapper 
        String pathandword = key.toString();
        String[] splitted = pathandword.split("\\*");
        String path = splitted[0];
        String word = splitted[1];  
        String filename=null;
        //From the path,we are taking last index,which indicate the filename/organism name
        int index=path.lastIndexOf('/');
        if(index>0){
            //Here we append the organism name with serach index or GO:term
            filename=path.substring(index+1)+"_"+word;
            }
            one.set(filename);
            result.set(sum);
            multipleoutputs.write(one,result , "final");

        }

        public void cleanup(Context context) throws IOException, InterruptedException {
            multipleoutputs.close();
        }
    }


        




public static void main(String[] args) throws Exception {
    //Initializing configuration
    Configuration conf = new Configuration();
    //Creating jobs for our MapReduce operation
    Job job = Job.getInstance(conf, "word count");

    String[] userargs = new GenericOptionsParser(conf, args).getRemainingArgs();

    job.setJarByClass(Bioinformatic_App.class);
    job.setMapperClass(TokenizerMapper.class);
    //job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setMapOutputKeyClass(Text.class);
    job.setMapOutputValueClass(IntWritable.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    job.setInputFormatClass(TextInputFormat.class);
    job.setOutputFormatClass(TextOutputFormat.class);

    FileInputFormat.addInputPath(job, new Path(userargs[0]));
    FileOutputFormat.setOutputPath(job, new Path(userargs[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
 

 }


}