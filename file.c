
{
   num = readln();
 
   if (num < 0) num = num * -1;
   else if (num > 0) num = num;
   else num = 0;
 
   while (num > 0) num = num - 2;
   println(num == 0);
}
