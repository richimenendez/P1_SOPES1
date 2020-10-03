/*
#include <linux/module.h>
#include <linux/init.h>
#include <linux/proc_fs.h>
#include <linux/sched.h>
#include <linux/uaccess.h>
#include <linux/fs.h>
#include <linux/sysinfo.h>
#include <linux/seq_file.h>
#include <linux/slab.h>
#include <linux/mm.h>
#include <linux/swap.h>
#include <linux/timekeeping.h>

static int my_proc_show(struct seq_file *m, void *v)
{
	struct task_struct *tareas;
	struct task_struct *hijos;
	struct list_head *head;
	int totalpor = 0;
	for_each_process(tareas)
	{

		if (tareas->utime > 0)
		{
			int cutime = 0;
			int cstime = 0;
			list_for_each(head, &tareas->children)
			{
				hijos = list_entry(head, struct task_struct, sibling);
				if (hijos->utime > 0)
				{
					cutime = cutime + hijos->utime;
					cstime = cstime + hijos->stime;
				}
			}


			int total_time = tareas->utime + tareas->stime + cutime + cstime;
			int segundos = tareas->utime - (tareas->start_time / 100);
			int porcentage = (100 * (total_time / 100)) / segundos;
			if (porcentage > 0)
			{
				totalpor = totalpor + porcentage;
			}
		}
	}
	seq_printf(m, "%d", totalpor);

	return 0;
}

static size_t my_proc_write(struct file *file, const char __user *buffer, size_t count, loff_t *f_pos)
{
	return 0;
}

static int my_proc_open(struct inode *inode, struct file *file)
{
	return single_open(file, my_proc_show, NULL);
}

static struct file_operations my_fops = {
	.owner = THIS_MODULE,
	.open = my_proc_open,
	.release = single_release,
	.read = seq_read,
	.llseek = seq_lseek,
	.write = my_proc_write};

static int __init test_init(void)
{
	struct proc_dir_entry *entry;
	entry = proc_create("test-module", 0777, NULL, &my_fops);
	if (!entry)
	{
		return -1;
	}
	else
	{
		printk(KERN_INFO "Inicio\n");
	}
	return 0;
}

static void __exit test_exit(void)
{
	remove_proc_entry("cpu-module", NULL);
	printk(KERN_INFO "Final\n");
	}

module_init(test_init);
module_exit(test_exit);
MODULE_LICENSE("GPL");
*/
// SPDX-License-Identifier: GPL-3.0
#include <linux/kernel.h>  // printk(), pr_*()
#include <linux/module.h>  // THIS_MODULE, MODULE_VERSION, ...
#include <linux/init.h>    // module_{init,exit}()
#include <linux/smp.h>     // get_cpu(), put_cpu()
#include <linux/cpufreq.h> // cpufreq_get()
#include <linux/cpumask.h> // cpumask_{first,next}(), cpu_online_mask

#ifdef pr_fmt
#undef pr_fmt
#endif
#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt

static int __init modinit(void)
{
        unsigned cpu = cpumask_first(cpu_online_mask);

        while (cpu < nr_cpu_ids) {
                seq_printf("CPU: %u, freq: %u kHz\n", cpu, cpufreq_get(cpu));
                cpu = cpumask_next(cpu, cpu_online_mask);
        }

        return 0;
}

static void __exit modexit(void)
{
        // Empty function only to be able to unload the module.
        return;
}

module_init(modinit);
module_exit(modexit);
MODULE_VERSION("0.1");
MODULE_DESCRIPTION("Get CPU frequency for currently online CPUs.");
MODULE_AUTHOR("Marco Bonelli");
MODULE_LICENSE("GPL");